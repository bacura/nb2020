#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 bond server 0.00b (2022/12/23)

#==============================================================================
#STATIC
#==============================================================================
@debug = false
#script = File.basename( $0, '.cgi' )

#==============================================================================
#LIBRARY
#==============================================================================
require './soul.rb'
require 'net/http'

#==============================================================================
#DEFINITION
#==============================================================================

class Res
  def initialize( cgi )
    @guset_url = cgi['myurl']
    @guset_open_nb = cgi['open_nb']
  end

  def hello( bond )
  #  unless $MYURL == guset_url
    unless false
      uri = URI.parse( @guset_url + 'printv.cgi' )
      res = Net::HTTP.get_response( uri )
      token = SecureRandom.base64( 10 )
      print token if res.code == '200'

      bond['token'] = token
      bond_ = JSON.generate( bond )
      mdb( "UPDATE #{$MYSQL_TB_MODJ} SET json='#{bond_}' WHERE module='nb' AND user='#{$GM}';", false, @debug )
    end
  end


  def db_cast( query )
    res_ = Hash.new
    r = mdb( query, false, @debug )
    r.each_with_index do |e, i|
      tj = JSON.generate( e )
      res_[i.to_s] = JSON.parse( tj )
    end
    print JSON.generate( res_ )

  end
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

command = @cgi['command']
token = @cgi['token']
res = Res.new( @cgi )

#urls = "#{$NBURL}\n"
r = mdb( "SELECT * FROM #{$MYSQL_TB_MODJ} WHERE module='nb' AND user='#{$GM}';", false, @debug )
if r.first
  if r.first['json'] != nil && r.first['json'] != ''
    bond = JSON.parse( r.first['json'] )
    urls = bond['urls']
    open_nb = bond['open'].to_i
    token_ = bond['token']
  end
end


res.hello( bond ) if command == 'res_hello'


exit( 9 ) if token != token_

case command
when 'res_fctp'
  res.db_cast( "SELECT * FROM fctp WHERE FN LIKE 'P%';" )
when 'res_tag'
  res.db_cast( "SELECT tag.* FROM tag INNER JOIN fctp ON fctp.FN = tag.FN WHERE fctp.FN LIKE 'P%';" )
when 'res_ext'
  res.db_cast( "SELECT ext.* FROM ext INNER JOIN fctp ON fctp.FN = ext.FN WHERE fctp.FN LIKE 'P%';" )
when 'order'
when 'receive'
when 'delivery'
when 'rev'
end

