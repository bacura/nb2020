#! /usr/bin/ruby
# coding: utf-8
#Nutrition browser 2020 login 0.02b (2022/11/07)


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'login'


#==============================================================================
#LIBRARY
#==============================================================================
require './probe'
require "./language_/#{script}.lp"


#==============================================================================
#DEFINITION
#==============================================================================

#### HTML login
def html_login_form( msg, l )
  html = <<-"HTML"
    <div class="container">
      <div class="row">
        <div class="col-6">
          <form action="login.cgi?mode=check" method="post" class="form-signin login_form">
          #{msg}
          <p class="msg_small">#{l['message']}</p>
          <input type="text" name="id" id="inputID" class="form-control login_input" placeholder="ID" required autofocus>
          <input type="password" name="pass" id="inputPassword" class="form-control login_input" placeholder="#{l['password']}">
          <input type="submit" value="#{l['login']}" class="btn btn-primary btn-block"></input>
          </form>
        </div>
        <div class="col-6">
          #{l['empty']}
        </div>
      </div>
    </div>
HTML

  puts html
end


#### Language init
#def lp_init( script, language_set )
#  f = open( "#{$HTDOCS_PATH}/language_/#{script}.#{language_set}", "r" )
#  lp = [nil]
#  f.each do |line|
#    lp << line.chomp.force_encoding( 'UTF-8' )
#  end
#  f.close
#
#  return lp
#end


#### HTML top
def html_top_login( l )
  login_color = "secondary"
  login = "<a href=\"regist.cgi\" class=\"text-#{login_color}\">#{l['regist']}</a>"

  html = <<-"HTML"
<header class="navbar navbar-expand-lg navbar-dark bg-dark" id="header">
  <div class="container-fluid">
    <a href="index.cgi" class="navbar-brand h1 text-#{login_color}">#{l['nb']}</a>
    <span class="navbar-text text-#{login_color} login_msg h4">#{login}</span>
    <a href='https://neg.bacura.jp/?page_id=1154' target='manual'>#{l['help']}</a>
    <span class="d-flex">
      <select class="form-select" id="qcate">
        <option value='0'>#{l['food']}</option>
        <option value='1'>#{l['recipe']}</option>
        <option value='2'>#{l['memory']}</option>
      </select>
      <input class="form-control" type="text" maxlength="100" id="words" onchange="search()">
      <btton class='btn btn-sm' onclick="search()">#{l['search']}</button>
    </span>
  </div>
</header>
HTML

  puts html
end

#==============================================================================
# Main
#==============================================================================
text_init() if @debug

#### Getting GET data
get_data = get_data()

#### Getting POST date
user = User.new( @cgi )
user.debug if @debug
#lp = lp_init( script, $DEFAULT_LP )
l = language_pack( $DEFAULT_LP )
#puts l if @debug


puts "#{get_data['mode']}" if @debug
case get_data['mode']
when 'check'
  #### Checking user ID on DB

  r = mdb( "SELECT user, status FROM #{$MYSQL_TB_USER} WHERE user='#{@cgi['id']}' AND pass='#{@cgi['pass']}' AND status>'0';", true, @debug )
  unless r.first
      html_init( nil )
      html_head( nil, 0, nil )
      html_top_login( lp )
      msg = "<p class='msg_small_red'>#{l['error']}</p>"
      html_login_form( msg, lp )
      html_foot()
  else
    status = r.first['status'].to_i

    # Issuing cookies
    uid = SecureRandom.hex( 16 )
    cookie = "Set-Cookie: NAME=#{@cgi['id']}\nSet-Cookie: #{$COOKIE_UID}=#{uid}\n"

    # Updating user information
    mdb( "UPDATE #{$MYSQL_TB_USER} SET cookie='#{uid}', cookie_m=NULL WHERE user='#{@cgi['id']}';", true, @debug )
    html_init( cookie )
    html_head( 'refresh', status, nil )
    puts '</span></body></html>'

    # Checking & repairing history table
    r = mdb( "SELECT user FROM #{$MYSQL_TB_HIS} WHERE user='#{@cgi['id']}';", false, @debug )
    mdb( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{@cgi['id']}', his='';", false, @debug )  unless r.first

    # Checking & repairing SUM table
    r = mdb( "SELECT user FROM #{$MYSQL_TB_SUM} WHERE user='#{@cgi['id']}';", false, @debug )
    mdb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{@cgi['id']}', sum='';", false, @debug ) unless r.first

    # Checking & repairing meal table
    r = mdb( "SELECT user FROM #{$MYSQL_TB_MEAL} WHERE user='#{@cgi['id']}';", false, @debug )
    mdb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{@cgi['id']}', meal='';", false, @debug ) unless r.first

    # Checking & repairing config table
    r = mdb( "SELECT user FROM #{$MYSQL_TB_CFG} WHERE user='#{@cgi['id']}';", false, @debug )
    mdb( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{@cgi['id']}', recipel='1:0:0:0:0:0:0';", false, @debug ) unless r.first
  end

when 'logout'
  # Meaningless Cookie
  cookie = "Set-Cookie: NAME=NULL\nSet-Cookie: #{$COOKIE_UID}=NULL\n"
  html_init( cookie )
  html_head( 'refresh', 0, nil )
  puts '</span></body></html>'
  mdb( "UPDATE #{$MYSQL_TB_USER} SET cookie_m=NULL WHERE user='#{user.name}';", true, @debug )

when 'family'
  cookie = ''
  login_mv = get_data['login_mv']
  puts "->#{login_mv}" if @debug
  r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{login_mv}';", true, @debug )
  if r.first
    puts r.first['mom'] if @debug
    if r.first['mom'] == '' ||  r.first['mom'] == nil
        cookie = "Set-Cookie: NAME=#{login_mv}\nSet-Cookie: #{$COOKIE_UID}=#{r.first['cookie']}\n"
        mdb( "UPDATE #{$MYSQL_TB_USER} SET cookie_m=NULL WHERE user='#{user.name}';", true, @debug )
    else
      rr = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user=\"#{r.first['mom']}\";", true, @debug )
      if rr.first
        # Issuing cookies
        uid = SecureRandom.hex( 16 )
        mid = rr.first['cookie']
        cookie = "Set-Cookie: NAME=#{login_mv}\nSet-Cookie: #{$COOKIE_UID}=#{uid}\n"
        puts cookie if @debug

        mdb( "UPDATE #{$MYSQL_TB_USER} SET cookie='#{uid}', cookie_m='#{mid}' WHERE user='#{login_mv}';", true, @debug )
        mdb( "UPDATE #{$MYSQL_TB_USER} SET cookie_m=NULL WHERE user='#{user.name}';", true, @debug )
      end
    end
  end
  html_init( cookie )

  html_head( 'refresh', r.first['status'], nil )
  puts '</span></body></html>'

# Input form init
else
  html_init( nil )
  html_head( nil, 0, nil )
  html_top_login( l )
  html_login_form( nil, l )
  html_foot()
end

