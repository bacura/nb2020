#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 recipe photo 0.4b (2024/01/02)

#==============================================================================
# STATIC
#==============================================================================
@debug = false
tmp_delete = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul'
require 'fileutils'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
	l = Hash.new

	#Japanese
	l['jp'] = {
		'camera'	=> "<img src='bootstrap-dist/icons/camera.svg' style='height:1.2em; width:1.2em;'>",\
		'trash'		=> "<img src='bootstrap-dist/icons/trash-fill.svg' style='height:1.2em; width:1.2em;'>",\
		'left-ca'	=> "<img src='bootstrap-dist/icons/arrow-left-circle.svg' style='height:1.2em; width:1.2em;'>",\
		'right-ca'	=> "<img src='bootstrap-dist/icons/arrow-right-circle.svg' style='height:1.2em; width:1.2em;'>"
	}

	return l[language]
end


def view_series( user, code, l, size )
	recipe = Recipe.new( user )
	recipe.load_db( code, true )

	media = Media.new( user.name )
	media.code = code
	media.load_series()

	if media.series.size > 0
		puts "<div class='row'>"
		media.series.each.with_index( 0 ) do |e, i|
			puts "<div class='col'>"
			if recipe.protect != 1 && media.muser == user.name
				puts "<span onclick=\"photoMove( '#{code}', '#{e}', #{i - 1} )\">#{l['left-ca']}</span>" if i != 0
				puts "&nbsp;&nbsp;<span onclick=\"photoMove( '#{code}', '#{e}', #{i + 1} )\">#{l['right-ca']}</span>" if i != media.series.size - 1
			end
			puts '<br>'
			puts "<a href='#{$PHOTO}/#{e}.jpg' target='photo'><img src='#{$PHOTO}/#{e}-tn.jpg' width='#{size}px' class='img-thumbnail'></a><br>"
			puts "<span onclick=\"photoDel( '#{code}', '#{e}', 'recipe' )\">#{l['trash']}</span>" if recipe.protect != 1 && media.muser == user.name
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
l = language_pack( user.language )
db = Db.new( user, @debug, false )


# POST
command = @cgi['command']
base = @cgi['base']
code = @cgi['code']
mcode = @cgi['mcode']
zidx = @cgi['zidx']
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "mcode: #{mcode}<br>"
	puts "zidx: #{zidx}<br>"
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
	end
	if query != ''
		r = db.query( query, false )
		code = r.first['code']
	end
end


case command
when 'upload'
	puts 'Upload<br>' if @debug
	if user.status != 7
		media = Media.new( user )
		media.code = code
		media.type = 'jpg'
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

#			puts "water mark<br>" if @debug
#			wm_text = "Nutrition Browser:#{media.mcode}"
#			wm_img = Magick::Image.new( photo.columns, photo.rows )
#			wm_drew = Magick::Draw.new
#			wm_drew.annotate( wm_img, 0, 0, 0, 0, wm_text ) do
#				self.gravity = Magick::SouthWestGravity
#				self.pointsize = 18
#				self.font_family = $WM_FONT
#				self.font_weight = Magick::BoldWeight
#				self.stroke = "none"
#			end
#			wm_img = wm_img.shade( true, 315 )
#			photo.composite!( wm_img, Magick::CenterGravity, Magick::HardLightCompositeOp )
			photo.write( "#{$PHOTO_PATH}/#{media.mcode}.jpg" )

			puts "insert DB<br>" if @debug
			media.load_series()
			media.save_db

			File.unlink "#{$TMP_PATH}/#{media.origin}" if File.exist?( "#{$TMP_PATH}/#{media.origin}" ) && tmp_delete
		end
	end

when 'move'
	if user.status != 7
		puts 'Move<br>' if @debug
		media = Media.new( user )
		media.code = code
		media.mcode = mcode
		media.zidx = zidx

		puts "Update DB<br>" if @debug
		media.load_series()
		media.move_series()
	end

when 'delete'
	if user.status != 7
		puts 'Delete<br>' if @debug
		File.unlink "#{$PHOTO_PATH}/#{mcode}-tns.jpg" if File.exist?( "#{$PHOTO_PATH}/#{mcode}-tns.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{mcode}-tn.jpg" if File.exist?( "#{$PHOTO_PATH}/#{mcode}-tn.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{mcode}.jpg" if File.exist?( "#{$PHOTO_PATH}/#{mcode}.jpg" )

		puts "delete item DB<br>" if @debug
		media = Media.new( user )
		media.mcode = mcode
		media.delete_db
	end
end

view_series( user, code, l, 200 )
puts "	<div align='right' class='code'>#{code}</div>"
