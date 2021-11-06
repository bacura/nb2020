#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser Lucky sum input driver 0.01b

#==============================================================================
#LIBRARY
#==============================================================================
require './probe'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'lucky'


#==============================================================================
#DEFINITION
#==============================================================================
class OI
	def initialize( line )
		@items = line.split( "\t" )
		@food_no = []
		@weight = []
		@unit = []
		@others = []

		@items.each do |e|
			if /\d?\d\d\d\d/ =~ e
				if e.size == 5
					@food_no << e
				else
					@food_no << "0#{e}"
				end
			elsif /\d|\.+/ =~ e
				@weight << BigDecimal( e )
			elsif /\[\w+\]/ =~ e
				@unit << e
			elsif e != ''
				@others << e
			end
		end
	end

	attr_accessor :items, :food_no, :weight, :unit, :others
end
#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
lp = user.load_lp( script )


#### Getting POST data
command = @cgi['command']
lucky_data = @cgi['lucky_data']
if @debug
	puts "command:#{command}<br>"
	puts "lucky_data:#{lucky_data}<br>"
	puts "<hr>"
end


####
html = ''
case command
when 'form'
	html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-10'>
			<h5>#{lp[1]}:</h5>
		</div>
		<div class='col-2'>
			<button type='button' class='btn btn-primary btn-sm' onclick=\"luckyAnalyze()\">#{lp[2]}</button>
		</div>
	</div>
	<br>
	<div class="input-group">
  		<div class="input-group-prepend">
			<span class="input-group-text">☆</span>
  		</div>
		<textarea class="form-control" aria-label="lucky_data" id="lucky_data"></textarea>
	</div>
</div>
HTML

# 解析
when 'analyze'
	candidate = nil

	# 特異データ検出
	candidate = 'eiyo_kun' if /\[5A食品コード\]/ =~ lucky_data

	unless candidate
		lucky_data.gsub!( "\r\n", "\n")
		lucky_data.gsub!( "\r", "\n")
		lucky_data.gsub!( /\n+/, "\n")
		lucky_data.gsub!( " ", "\t")
		lucky_data.gsub!( "　", "\t")
		lucky_data.gsub!( ",", "\t")
		lucky_data.gsub!( '．', '.')
		lucky_data.tr!( "０-９", "0-9" )
		lucky_data.gsub!( /g|G/, "\t[g]" )
		lucky_data.gsub!( /ｇ|G/, "\t[g]" )
		lucky_data.gsub!( 'グラム', "\t[g]" )
		lucky_data.gsub!( /c|Cu|Up|P/, "\t[cup]" )
		lucky_data.gsub!( /ｃ|Cｕ|Ｕｐ|Ｐ/, "\t[cup]" )
		lucky_data.gsub!( 'カップ', "\t[cup]" )
		lucky_data.gsub!( /m|Ml|L/, "\t[ml]" )
		lucky_data.gsub!( /ｍ|Ｍｌ|Ｌ/, "\t[ml]" )
		lucky_data.gsub!( 'c|Cc|C', "\t[cc]" )
		lucky_data.gsub!( 'd|Dl|l', "\t[dl]" )
		lucky_data.gsub!( '大さじ', "\t[bs]" )
		lucky_data.gsub!( 'おおさじ', "\t[bs]" )
		lucky_data.gsub!( '小さじ', "\t[ss]" )
		lucky_data.gsub!( 'こさじ', "\t[ss]" )
		lucky_data.gsub!( /\t+/, "\t")
		lucky_line = lucky_data.split( "\n" )
		lucky_solid = []
		lucky_line.each do |e| lucky_solid << OI.new( e ) end

		simple_flag = true
		lucky_solid.each do |e|
			simple_flag = false unless e.food_no.size <= 1 && e.weight.size <= 1 && e.unit.size <= 1
		end
		candidate = 'general' if simple_flag
	end
	puts "candidate:#{candidate}<br>" if @debug

	case candidate
	when 'eiyo_kun'
		require "#{$HTDOCS_PATH}/lucky_/eiyo_kun.rb"
	when 'general'
		require "#{$HTDOCS_PATH}/lucky_/general.rb"
	else
		require "#{$HTDOCS_PATH}/lucky_/oi.rb"
	end

	r = add2cb( lucky_solid, user.name )
end

puts html
