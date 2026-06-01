# frozen_string_literal: true
# Jekyll 빌드 전에 실행: bundle exec ruby tools/generate_og_images.rb

require 'yaml'
require 'date'
require 'fileutils'
require 'json'

ROOT       = File.expand_path('..', __dir__)
POSTS_DIR  = File.join(ROOT, '_posts')
OUTPUT_DIR = File.join(ROOT, 'assets', 'img', 'og', 'posts')
PY_SCRIPT  = File.join(ROOT, 'tools', 'generate_og_images.py')

FileUtils.mkdir_p(OUTPUT_DIR)

generated = 0
errors    = 0

Dir.glob(File.join(POSTS_DIR, '**', '*.{md,markdown}')).sort.each do |post_file|
  content = File.read(post_file, encoding: 'utf-8')
  next unless content =~ /\A---\s*\n(.*?)\n---\s*\n/m

  front_matter = YAML.safe_load($1, permitted_classes: [Date, Time, DateTime]) rescue YAML.safe_load($1) rescue {}
  title = front_matter['title'].to_s
  tags  = Array(front_matter['tags']).map { |t| "##{t}" }.join('  ·  ')
  date  = if front_matter['date']
             Date.parse(front_matter['date'].to_s).strftime('%Y.%m.%d') rescue ''
           elsif File.basename(post_file) =~ /^(\d{4}-\d{2}-\d{2})/
             Date.parse($1).strftime('%Y.%m.%d') rescue ''
           else
             ''
           end

  slug        = File.basename(post_file, '.*').sub(/^\d{4}-\d{2}-\d{2}-/, '')
  output_path = File.join(OUTPUT_DIR, "#{slug}.png")

  if File.exist?(output_path)
    puts "  건너뜀 (이미 존재): #{File.basename(output_path)}"
    next
  end

  begin
    data = JSON.generate({ title: title, tags: tags, date: date, output_path: output_path })
    system('python3', PY_SCRIPT, data) or raise 'Python 스크립트 실패'
    puts "  ✓ #{File.basename(output_path)}"
    generated += 1
  rescue => e
    warn "  ✗ #{slug}: #{e.message}"
    errors += 1
  end
end

puts "\nOG 이미지 생성 완료: #{generated}개 생성, #{errors}개 실패"
exit(1) if errors > 0
