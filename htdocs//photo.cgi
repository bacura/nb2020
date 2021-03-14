#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe photo 0.00b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script = 'photo'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================
def view_series( user, code, lp )
	puts "view_series( #{user}, #{code} )<br>" if @debug
	media_code = []
	r = mdb( "SELECT mcode FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND code='#{code}';", false, @debug )
	if r.first
		r.each do |e| media_code << e['mcode'] end
		puts "#{media_code}<br>" if @debug

		puts 'View code series<br>' if @debug
		puts "<div class='row'>"
		media_code.each do |e|
			puts "<div class='col'>"
			puts "<span onclick=\"photoDel( '#{code}', '#{e}' )\">#{lp[1]}</span><br>"
			puts "<img src='#{$PHOTO}/#{e}-tn.jpg' width='200px' class='img-thumbnail'>"
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
	puts "PHOTO_PATH: #{$PHOTO_PATH}<br>"
	puts "<hr>"
end


puts 'base code<br>' if @debug
if code == ''
	query = ''
	if base == 'menu'
		query = "SELECT code FROM #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';"
	else
		query = "SELECT code FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';"
	end
	r = mdb( query, false, @debug )
	code = r.first['code']
end


case command
when 'view_series'
	view_series( user, code, lp )

when 'upload'
	puts 'Upload<br>' if @debug
	photo_name = @cgi['photo'].original_filename
	photo_type = @cgi['photo'].content_type
	photo_body = @cgi['photo'].read
	photo_size = photo_body.size.to_i
	if @debug
		puts "#{photo_name}<br>"
		puts "#{photo_type}<br>"
		puts "#{photo_size}<br>"
		puts "<hr>"
	end

	if photo_size < $SIZE_MAX && ( photo_type == 'image/jpeg' || photo_type == 'image/jpg' )
		require 'nkf'
		require 'rmagick'

		puts "temporary file<br>" if @debug
		f = open( "#{$TMP_PATH}/#{photo_name}", 'w' )
		f.puts photo_body
		f.close
		mcode = generate_code( user.name, 'p' )
		photo = Magick::ImageList.new( "#{$TMP_PATH}/#{photo_name}" )

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
		tn_file.write( "#{$PHOTO_PATH}/#{mcode}-tn.jpg" )

		puts "small SN resize<br><br>" if @debug
		tns_file = photo.thumbnail( tns_ratio )
		tns_file.write( "#{$PHOTO_PATH}/#{mcode}-tns.jpg" )

		puts "resize 2k<br>" if @debug
		photo = photo.thumbnail( photo_ratio ) if photo_ratio != 1.0

		puts "water mark<br>" if @debug
		wm_text = "NB2020 #{code} by #{user.name}"
#		wm_text = "食品成分表ブラウザ 2015\nPhoto by #{user.name} in #{#DATETIME.year}"
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
		photo.write( "#{$PHOTO_PATH}/#{mcode}.jpg" )

		puts "insert DB<br>" if @debug
		mdb( "INSERT INTO #{$MYSQL_TB_MEDIA} SET user='#{user.name}', code='#{code}', mcode='#{mcode}', origin='#{photo_name}', date='#{@datetime}';", false, @debug )
	end
	view_series( user, code, lp )

#### 写真を削除
when 'delete'
	puts 'Delete<br>' if @debug
	File.unlink "#{$PHOTO_PATH}/#{mcode}-tns.jpg" if File.exist?( "#{$PHOTO_PATH}/#{mcode}-tns.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{mcode}-tn.jpg" if File.exist?( "#{$PHOTO_PATH}/#{mcode}-tn.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{mcode}.jpg" if File.exist?( "#{$PHOTO_PATH}/#{mcode}.jpg" )

	puts "delete item DB<br>" if @debug
	mdb( "DELETE FROM #{$MYSQL_TB_MEDIA} WHERE user='#{user.name}' AND mcode='#{mcode}';", false, @debug )
	view_series( user, code, lp )
end

puts "	<div align='right' class='code'>#{code}</div>"
