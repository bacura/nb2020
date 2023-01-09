#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 GM bond cliant 0.00b (2022/12/23)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )
server = 'bond-server.cgi'

#==============================================================================
#LIBRARY
#==============================================================================
require './soul.rb'
require 'net/http'

#==============================================================================
#DEFINITION
#==============================================================================

# Language pack
def language_pack( language )
  l = Hash.new

  #Japanese
  l['jp'] = {
    'bond'    => "絆",\
    'onbs'  => "他所の栄養ブラウザURL",\
    'cross'  => "交信を試みる",\
    'open'  => "相互交信",\
    'condition' => "状態管理",\
  }

  return l[language]
end


def res2db( json, table, pkey )
  resh = JSON.parse( json )
  resh.each do |k, v|
    sql_set = ''
    r = mdb( "SELECT #{pkey} FROM #{table} WHERE #{pkey}='#{v[pkey]}';", false, @debug )
    if r.first
      v.each do |kk, vv|
        sql_set << "#{kk}='#{vv}'," if kk != pkey
      end
      sql_set.chop!
      mdb( "UPDATE #{table} SET #{sql_set} WHERE #{pkey}='#{resh[pkey]}';", false, @debug )

    else
      if v[pkey] != nil
        v.each do |kk, vv|
          sql_set << "#{kk}='#{vv}',"
        end
        sql_set.chop!
        mdb( "INSERT INTO #{table} SET #{sql_set};", false, @debug )
      end
    end
  end

  return resh.size
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

user = User.new( @cgi )
user.debug if @debug
l = language_pack( user.language )
bond = Hash.new


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### POST
command = @cgi['command']
urls = @cgi['urls'] if @cgi['urls'] != nil && @cgi['urls'] != ''
open_nb = @cgi['open_nb'].to_i if @cgi['open_nb'] != nil && @cgi['open_nb'] != ''
if @debug
  puts "command:#{command}<br>\n"
  puts "urls:#{urls}<br>\n"
  puts "open_nb:#{open_nb}<br>\n"
  puts "<hr>\n"
end


puts "LOAD config<br>" if @debug
#urls = "#{$NBURL}\n"
if command == 'init'
  r = mdb( "SELECT * FROM #{$MYSQL_TB_MODJ} WHERE module='nb' AND user='#{user.name}';", false, @debug )
  if r.first
    if r.first['json'] != nil && r.first['json'] != ''
      bond = JSON.parse( r.first['json'] )
      urls = bond['urls']
      open_nb = bond['open'].to_i
    end
  end
end

if command == 'cross'
  bond['urls'] = urls
  bond['open_nb'] = open_nb
  bond_ = JSON.generate( bond )
  mdb( "UPDATE #{$MYSQL_TB_MODJ} SET json='#{bond_}' WHERE user='#{$GM}' AND module='nb';", false, @debug )

  puts "<h6>Console</h6><br>"
  # start talk
  urls = @cgi['urls'].split( "\n" )
#  urls.delete( $MYURL )
  open_nb = @cgi['open_nb'].to_i
  post_data = { command:'res_hello', myurl:$MYURL, open_nb:@cgi['open_nb'] }

urls[0] = $NBURL
  urls.each do |e|
#    uri = URI.parse( e + server )
    uri = URI.parse( $MYURL + server )
    res = Net::HTTP.post_form( uri, post_data )
    puts "[#{e}] #{res.code} res_hello"
    exit( 9 ) if res.body == ''
    puts "[#{res.body}]<br>"
    token = res.body

    #bond to fctp
    post_data = { command:'res_fctp', myurl:$MYURL, token:token }
    res = Net::HTTP.post_form( uri, post_data )
#    exit( 9 ) if res.body != ''
    puts "[#{e}] #{res.code} res_fctp"
    res.body.force_encoding( 'utf-8' )
    res_size = res2db( res.body, $MYSQL_TB_FCTP, 'FN' )
    puts "[#{res_size}]<br>"

    #bond to tag
    post_data = { command:'res_tag', myurl:$MYURL, token:token }
    res = Net::HTTP.post_form( uri, post_data )
#    exit( 9 ) if res.body != ''
    puts "[#{e}] #{res.code} res_tag"
    res.body.force_encoding( 'utf-8' )
    res_size = res2db( res.body, $MYSQL_TB_TAG, 'FN' )
    puts "[#{res_size}]<br>"

    #bond to ext
    post_data = { command:'res_ext', myurl:$MYURL, token:token }
    res = Net::HTTP.post_form( uri, post_data )
#    exit( 9 ) if res.body != ''
    puts "[#{e}] #{res.code} res_ext"
    res.body.force_encoding( 'utf-8' )
    res_size = res2db( res.body, $MYSQL_TB_EXT, 'FN' )
    puts "[#{res_size}]<br>"





#    res2db_food( ext_, $MYSQL_TB_EXT, 'FN' )

  end
  exit( 0 )
end


open_checked = ''
open_checked = 'CHECKED' if open_nb == 1

html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
    <div class='col-8'><h5>#{l['bond']}: #{$MYURL}</h5></div>
    <div class='col-2 form-check form-switch'>
      <input class="form-check-input" type="checkbox" id="open_nb" #{open_checked}>
      <label class="form-check-label">#{l['open']}</label>
    </div>
    <div class='col-2' align='right'>
      <button class="btn btn-sm btn-danger" onclick="crossBond()">#{l['cross']}</button>
    </div>
	</div>
	<div class='row'>
    <label class="form-label">#{l['urls']}</label>
		<textarea class="form-control" id='urls' rows="10">#{urls}</textarea>
	</div>
</div>


HTML

puts html
