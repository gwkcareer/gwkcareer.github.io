# frozen_string_literal: true
# Jekyll 렌더링 전에 포스트마다 og:image 경로를 설정합니다.
# 실제 PNG 파일은 tools/generate_og_images.rb 에서 생성됩니다.

module Jekyll
  class OgImageDataGenerator < Generator
    safe true
    priority :lowest

    def generate(site)
      site.posts.docs.each do |post|
        next if post.data['image']
        slug = post.data['slug'] || post.basename_without_ext
        # Chirpy 테마: image.path 형식을 사용해야 커버 이미지로 표시되지 않음
        post.data['image'] = { 'path' => "/assets/img/og/posts/#{slug}.png" }
      end
    end
  end
end
