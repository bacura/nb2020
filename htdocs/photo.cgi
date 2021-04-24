#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe photo 0.02b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'
require 'fileutils'


#==============================================================================
#STATIC
#==============================================================================
script = 'photo'
@debug = false
tmp_delete = false


#==============================================================================
#DEFINITION
#==============================================================================
def view_series( user, code, del_icon, size )
	media = Media.new( user )
	media.code = code
	media.load_series()

	if media.series.size > 0
		puts "<div class='row'>"
		media.series.each do |e|
			puts "<div class='col'>"
			puts "<span onclick=\"photoDel( '#{code}', '#{e}', 'recipe' )\">#{del_icon}</span><br>"
			puts "<a href='#{$PHOTO}/#{e}.jpg' target='photo'><img src='#{$PHOTO}/#{e}-tn.jpg' width='#{size}px' class='img-thumbnail'></a>"
			puts "</div>"
		end
		puts "</div>"
	else
		puts 'No photo'
	end
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


# POST
command = @cgi['command']
base= @cgi['base']
code = @cgi['code']
mcode = @cgi['mcode']
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "mcode: #{mcode}<br>"
	puts "base: #{base}<br>"
	puts "PHOTO_PATH: #{$PHOTO_PATH}<br>"
	puts "<hr>"
end


puts 'base code<br>' if @debug
if code == ''
	query = ''
	case base
	when 'menu'
		query = "SELECT code FROM #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';"
	when 'recipe'
		query = "SELECT code FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';"
	when 'koyomi'
	end
	r = mdb( query, false, @debug )
	code = r.first['code']
end


case command
when 'view_series'
	puts 'View series<br>' if @debug
	view_series( user, code, lp[1], 200 )

when 'upload'
	puts 'Upload<br>' if @debug
	media = Media.new( user )
	media.code = code
	media.date = @datetime

	media.origin = @cgi['photo'].original_filename
	photo_type = @cgi['photo'].content_type
	photo_body = @cgi['photo'].read
	photo_size = photo_body.size.to_i
	if @debug
		puts "#{media.origin}<br>"
		puts "#{photo_type}<br>"
		puts "#{photo_size}<br>"
		puts "<hr>"
	end

	if photo_size < $SIZE_MAX && ( photo_type == 'image/jpeg' || photo_type == 'image/jpg' )
		puts 'Image magick<br>' if @debug
		require 'nkf'
		require 'rmagick'

		puts "temporary file<br>" if @debug
		f = open( "#{$TMP_PATH}/#{media.origin}", 'w' )
		f.puts photo_body
		f.close
		media.mcode = generate_code( user.name, 'p' )
		photo = Magick::ImageList.new( "#{$TMP_PATH}/#{media.origin}" )

		puts "Resize<br>" if @debug
		photo_x = photo.columns.to_f
		photo_y = photo.rows.to_f
		photo_ratio = 1.0
		if photo_x >= photo_y
			tn_ratio = $TN_SIZE / photo_x
			tns_ratio = $TNS_SIZE / photo_x
			photo_ratio = $PHOTO_SIZE_MAX / photo_x if photo_x >= $PHOTO_SIZE_MAX
		else
			tn_ratio = $TN_SIZE / photo_y
			tns_ratio = $TNS_SIZE / photo_y
			photo_ratio = $PHOTO_SIZE_MAX / photo_y if photo_y >= $PHOTO_SIZE_MAX
		end

		puts "medium SN resize<br>" if @debug
		tn_file = photo.thumbnail( tn_ratio )
		tn_file.write( "#{$PHOTO_PATH}/#{media.mcode}-tn.jpg" )

		puts "small SN resize<br><br>" if @debug
		tns_file = photo.thumbnail( tns_ratio )
		tns_file.write( "#{$PHOTO_PATH}/#{media.mcode}-tns.jpg" )

		puts "resize 2k<br>" if @debug
		photo = photo.thumbnail( photo_ratio ) if photo_ratio != 1.0

		puts "water mark<br>" if @debug
		wm_text = "NB2020 #{code} by #{user.name}"
		wm_img = Magick::Image.new( photo.columns, photo.rows )
		wm_drew = Magick::Draw.new
		wm_drew.annotate( wm_img, 0, 0, 0, 0, wm_text ) do
			self.gravity = Magick::SouthWestGravity
			self.pointsize = 72
			self.font_family = $WM_FONT
			self.font_weight = Magick::BoldWeight
			self.stroke = "none"
		end
		wm_img = wm_img.shade( true, 315 )
		photo.composite!( wm_img, Magick::CenterGravity, Magick::HardLightCompositeOp )
		photo.write( "#{$PHOTO_PATH}/#{media.mcode}.jpg" )

		puts "insert DB<br>" if @debug
		media.save_db

		File.unlink "#{$TMP_PATH}/#{media.origin}" if File.exist?( "#{$TMP_PATH}/#{media.origin}" ) && tmp_delete
	end
	view_series( user, code, lp[1], 200 )

when 'delete'
	puts 'Delete<br>' if @debug
	File.unlink "#{$PHOTO_PATH}/#{mcode}-tns.jpg" if File.exist?( "#{$PHOTO_PATH}/#{mcode}-tns.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{mcode}-tn.jpg" if File.exist?( "#{$PHOTO_PATH}/#{mcode}-tn.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{mcode}.jpg" if File.exist?( "#{$PHOTO_PATH}/#{mcode}.jpg" )

	puts "delete item DB<br>" if @debug
	media = Media.new( user )
	media.mcode = mcode
	media.delete_db
	view_series( user, code, lp[1], 200 )
end

puts "	<div align='right' class='code'>#{code}</div>"
