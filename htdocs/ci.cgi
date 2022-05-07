#! /usr/bin/ruby
# coding: utf-8

if ENV['QUERY_STRING'] == nil
	puts "Content-type: text/text\n"
	puts "\n"
	puts 'non QUERY_STRING'
end

( width_, height_, img_id ) = ENV['QUERY_STRING'].split( '&' )

( k, width ) = width_.split( '=' )
( k, height ) = height_.split( '=' )

img_width = 1360;
img_height = 908;
if( width < height )
	img_width = 900;
	img_height = 1600;
end


rw = width.to_f / img_width
rh = height.to_f / img_height
zoom = 100
if( rw > rh )
	zoom = 100 * rw
else
	zoom = 100 * rh
end
zoom = 100 if zoom < 100


m = ''
m = 'm' if width.to_i < height.to_i
t = Time.now
mon = t.month
mon = "0#{mon}" if mon.to_i < 10
img_path = "img/#{mon}#{m}"


file_list = Dir.glob( "/var/www/htdocs/#{img_path}/*" )
exit if file_list.size == 0
file_list.shuffle!
file_list.shuffle!

t = File.basename( file_list[0] )
puts "<img src='#{img_path}/#{t}' class='d-block' id='#{img_id}' style='width:#{zoom.to_i}%;'>"
