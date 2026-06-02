import { Client } from "@notionhq/client";
import { NotionToMarkdown } from "notion-to-md";
import fs from "fs";
import path from "path";
import crypto from "crypto";
import https from "https";
import http from "http";

const NOTION_TOKEN = process.env.NOTION_TOKEN;
const NOTION_DATABASE_ID = process.env.NOTION_DATABASE_ID;
import { fileURLToPath } from "url";
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, "..");
const POSTS_DIR = path.join(ROOT_DIR, "_posts");
const IMAGES_DIR = path.join(ROOT_DIR, "assets/images");
const LAST_SYNC_FILE = path.join(ROOT_DIR, "notion-sync/last_sync.json");

const notion = new Client({ auth: NOTION_TOKEN });
const n2m = new NotionToMarkdown({ notionClient: notion });

function loadLastSync() {
  try {
    const data = JSON.parse(fs.readFileSync(LAST_SYNC_FILE, "utf8"));
    return data.last_sync || null;
  } catch {
    return null;
  }
}

function saveLastSync(time) {
  fs.writeFileSync(LAST_SYNC_FILE, JSON.stringify({ last_sync: time }, null, 2));
}

function sanitizeCategory(name) {
  return name.replace(/\(.*?\)/g, "").trim();
}

function slugify(text) {
  return text
    .toLowerCase()
    .replace(/[가-힣]+/g, (match) => {
      // 한글은 romanize 없이 그냥 제거 후 영문/숫자만 남김
      return "";
    })
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    || "post";
}

function downloadImage(url, destPath) {
  return new Promise((resolve) => {
    if (fs.existsSync(destPath)) {
      resolve(true);
      return;
    }
    const protocol = url.startsWith("https") ? https : http;
    const file = fs.createWriteStream(destPath);
    protocol.get(url, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close();
        fs.unlinkSync(destPath);
        downloadImage(res.headers.location, destPath).then(resolve);
        return;
      }
      res.pipe(file);
      file.on("finish", () => { file.close(); resolve(true); });
    }).on("error", () => {
      file.close();
      if (fs.existsSync(destPath)) fs.unlinkSync(destPath);
      resolve(false);
    });
  });
}

function getImageExt(url) {
  const clean = url.split("?")[0];
  const ext = path.extname(clean).toLowerCase();
  return [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"].includes(ext) ? ext : ".jpg";
}

async function processImage(url) {
  if (!url) return null;
  const hash = crypto.createHash("md5").update(url).digest("hex");
  const ext = getImageExt(url);
  const filename = `${hash}${ext}`;
  const destPath = path.join(IMAGES_DIR, filename);
  const localPath = `/assets/images/${filename}`;

  const ok = await downloadImage(url, destPath);
  return ok ? localPath : url;
}

function extractProp(page, name, type) {
  const prop = page.properties[name];
  if (!prop) return null;
  if (type === "title") return prop.title?.map((t) => t.plain_text).join("") || "";
  if (type === "rich_text") return prop.rich_text?.map((t) => t.plain_text).join("") || "";
  if (type === "select") return prop.select?.name || null;
  if (type === "multi_select") return prop.multi_select?.map((s) => s.name) || [];
  if (type === "date") return prop.date?.start || null;
  if (type === "status") return prop.status?.name || null;
  return null;
}

async function getFirstImage(pageId) {
  try {
    const blocks = await notion.blocks.children.list({ block_id: pageId });
    for (const block of blocks.results) {
      if (block.type === "image") {
        const img = block.image;
        return img.type === "file" ? img.file.url : img.external?.url || null;
      }
    }
  } catch {}
  return null;
}

async function buildMarkdown(pageId) {
  const mdBlocks = await n2m.pageToMarkdown(pageId);
  let mdString = n2m.toMarkdownString(mdBlocks).parent || "";

  // 이미지 URL 치환
  const imgRegex = /!\[.*?\]\((https?:\/\/[^\)]+)\)/g;
  const matches = [...mdString.matchAll(imgRegex)];
  for (const match of matches) {
    const originalUrl = match[1];
    const localPath = await processImage(originalUrl);
    if (localPath && localPath !== originalUrl) {
      mdString = mdString.replace(originalUrl, localPath);
    }
  }

  return mdString;
}

async function syncPages() {
  fs.mkdirSync(POSTS_DIR, { recursive: true });
  fs.mkdirSync(IMAGES_DIR, { recursive: true });

  const lastSync = loadLastSync();
  const nowTime = new Date().toISOString();

  const queryParams = {
    database_id: NOTION_DATABASE_ID,
    filter: {
      property: "상태",
      status: { equals: "완료" },
    },
    sorts: [{ property: "작성일", direction: "descending" }],
  };

  if (lastSync) {
    queryParams.filter = {
      and: [
        queryParams.filter,
        { timestamp: "last_edited_time", last_edited_time: { on_or_after: lastSync } },
      ],
    };
  }

  const response = await notion.databases.query(queryParams);
  const pages = response.results;

  if (pages.length === 0) {
    console.log("변경된 페이지 없음");
    console.log("SYNC_RESULT=post 등록 0건 / 업데이트 0건");
    saveLastSync(nowTime);
    return 0;
  }

  console.log(`${pages.length}개 페이지 처리 중...`);
  let newCount = 0;
  let updateCount = 0;

  for (const page of pages) {
    try {
      const title = extractProp(page, "제목", "title");
      const description = extractProp(page, "요약", "rich_text") || "";
      const dateStr = extractProp(page, "작성일", "date") || page.created_time.slice(0, 10);
      const upperCat = extractProp(page, "상위 카테고리", "select") || "";
      const lowerCat = extractProp(page, "하위 카테고리", "select") || "";
      const tags = extractProp(page, "태그", "multi_select") || [];

      // 본문 첫 이미지를 썸네일로
      const firstImgUrl = await getFirstImage(page.id);
      const thumbnail = firstImgUrl ? await processImage(firstImgUrl) : null;

      const slug = slugify(title) || page.id.slice(0, 8);
      const dateForFile = dateStr.slice(0, 10);
      const filename = `${dateForFile}-${slug}.md`;
      const filepath = path.join(POSTS_DIR, filename);

      const categories = [upperCat, lowerCat].filter(Boolean).map(sanitizeCategory);
      const categoriesStr = categories.map((c) => `"${c}"`).join(", ");
      const tagsStr = tags.map((t) => `"${t}"`).join(", ");
      const thumbnailLine = thumbnail ? `\nthumbnail: ${thumbnail}` : "";

      const mdContent = await buildMarkdown(page.id);

      const frontmatter = `---
layout: post
title: "${title.replace(/"/g, '\\"')}"
description: "${description.replace(/"/g, '\\"')}"${thumbnailLine}
date: ${dateForFile}
categories: [${categoriesStr}]
tags: [${tagsStr}]
---

${mdContent}`;

      const isNew = !fs.existsSync(filepath);
      fs.writeFileSync(filepath, frontmatter, "utf8");
      console.log(`✅ ${filename}`);
      if (isNew) newCount++; else updateCount++;
    } catch (err) {
      console.error(`❌ 페이지 처리 실패 (${page.id}):`, err.message);
    }
  }

  saveLastSync(nowTime);
  console.log(`완료: 신규 ${newCount}건 / 업데이트 ${updateCount}건`);
  console.log(`SYNC_RESULT=post 등록 ${newCount}건 / 업데이트 ${updateCount}건`);
  return newCount + updateCount;
}

syncPages().catch((err) => {
  console.error("동기화 실패:", err);
  process.exit(1);
});
