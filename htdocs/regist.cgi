#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser 2020 regist 0.01b

#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
script='regist'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### HTML top
def html_top_regist( lp )
  login_color = "secondary"
  login = "<a href='login.cgi' class=\"text-#{login_color}\">#{lp[17]}</a>"

  html = <<-"HTML"
<header class="navbar navbar-expand-lg navbar-dark bg-dark" id="header">
  <div class="container-fluid">
    <a href="index.cgi" class="navbar-brand h1 text-#{login_color}">#{lp[25]}</a>
    <span class="navbar-text text-#{login_color} login_msg h4">#{login}</span>
    <a href='https://neg.bacura.jp/?page_id=1154' target='manual'>#{lp[26]}</a>
    <span class="d-flex">
      <select class="form-select" id="qcate">
        <option value='0'>#{lp[28]}</option>
        <option value='1'>#{lp[29]}</option>
        <option value='2'>#{lp[20]}</option>
      </select>
      <input class="form-control" type="text" maxlength="100" id="words" onchange="search()">
      <btton class='btn btn-sm' onclick="search()">#{lp[27]}</button>
    </span>
  </div>
</header>
HTML

  puts html
end


#### Language init
def lp_init( script, language_set )
  f = open( "#{$HTDOCS_PATH}/language_/#{script}.#{language_set}", "r" )
  lp = [nil]
  f.each do |line|
    lp << line.chomp.force_encoding( 'UTF-8' )
  end
  f.close

  return lp
end


#### HTML regist
def html_regist_form( id, mail, pass, msg, aliasu, lp )
  option_language = ''
  $LP.each do |e|
    option_language << "<option value='#{e}'>#{e}</option>"
  end
  html = <<-"HTML"
      <div class="container">
        <form action="regist.cgi?mode=confirm" method="post" class="form-signin login_form">
          #{msg}
          <p class="msg_small">#{lp[4]}</p>
          <input type="text" name="id" value="#{id}" maxlength="30" class="form-control login_input" placeholder="#{lp[5]}" required autofocus>
          <input type="text" name="pass" value="#{pass}" maxlength="30" class="form-control login_input" placeholder="#{lp[8]}" required>
          <input type="text" name="aliasu" value="#{aliasu}" maxlength="60" class="form-control login_input" placeholder="#{lp[6]}">
          <input type="email" name="mail" value="#{mail}" maxlength="60" class="form-control login_input" placeholder="#{lp[7]}">
          <select name="language" class="form-select">
            #{option_language}
          </select>
          <br>
          <input type="submit" value="#{lp[9]}" class="btn btn-success btn-block"></input>
        </form>
      </div>

      <hr>
      <div  class="container" id='rule'></div>
      <script>$( function(){ $( "#rule" ).load( "books/guide/rule.html" );} );</script>
HTML

  puts html
end


#### HTML regist confirm
def html_regist_confirm( id, mail, pass, aliasu, language, lp )
    html = <<-"HTML"
      <div class="container">
        <form action="regist.cgi?mode=finish" method="post" class="form-signin login_form">
          <p class="msg_small">#{lp[10]}</p>
          <table class="table">
              <tr>
                <td>#{lp[11]}</td>
                <td>#{id}</td>
              </tr>
              <tr>
                <td>#{lp[14]}</td>
                <td>#{pass}</td>
              </tr>
              <tr>
                <td>#{lp[12]}</td>
                <td>#{aliasu}</td>
              </tr>
              <tr>
                <td>#{lp[13]}</td>
                <td>#{mail}</td>
              </tr>
              <tr>
                <td>#{lp[31]}</td>
                <td>#{language}</td>
              </tr>
          </table>
          <input type="hidden" name="id" value="#{id}">
          <input type="hidden" name="alias" value="#{aliasu}">
          <input type="hidden" name="mail" value="#{mail}">
          <input type="hidden" name="pass" value="#{pass}">
          <input type="hidden" name="language" value="#{language}">
          <input type="submit" value="#{lp[15]}" class="btn btn-warning btn-block"></input>
          <input type="button" value="#{lp[19]}" class="btn btn-secondary btn-block" onclick="history.back()"></input>
        </form>
      </div>
HTML

  puts html
end


#### HTML regist finish
def html_regist_finish( lp )
    html = <<-"HTML"
      <div class="container">
          <p class="reg_msg">#{lp[16]}<a href="login.cgi">#{lp[17]}<a/>#{lp[18]}</p>
      </div>
HTML

  puts html
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

lp = lp_init( 'regist', $DEFAULT_LP )

#### Getting GET data
get_data = get_data()

html_head( nil, 0, nil )
html_top_regist( lp )

case get_data['mode']
# Confomation of user data
when 'confirm'

  # Checking improper characters
  if /[^0-9a-zA-Z\-\_]/ =~ @cgi['id']
    msg = "<p class='msg_small_red'>#{lp[1]}</p>"
    html_regist_form( nil, @cgi['mail'], nil, msg, @cgi['aliasu'], lp )

  # Checking character limit
  elsif @cgi['id'].size > 30
    msg = "<p class='msg_small_red'>#{lp[2]}</p>"
    html_regist_form( nil, @cgi['mail'], nil, msg, @cgi['aliasu'], lp )

  # OK
  else
    # Checking same ID
    r = mdb( "SELECT user FROM #{$MYSQL_TB_USER} WHERE user='#{@cgi['id']}';", false, @debug )
    unless r.first
      html_regist_confirm( @cgi['id'], @cgi['mail'], @cgi['pass'], @cgi['aliasu'], @cgi['language'], lp )
    else
      msg = "<p class='msg_small_red'>#{lp[3]}</p>"
      html_regist_form( nil, @cgi['mail'], nil, msg, @cgi['aliasu'], lp )
    end
  end


#### Finishing registration of new user
when 'finish'
  # Inserting user information
  aliasu = @cgi['alias']
  aliasu = @cgi['id'] if aliasu == ''
  p @cgi if @debug

  mdb( "INSERT INTO #{$MYSQL_TB_USER} SET user='#{@cgi['id']}', pass='#{@cgi['pass']}', mail='#{@cgi['mail']}',aliasu='#{aliasu}', status=1, language='#{@cgi['language']}', reg_date='#{@datetime}'", false, @debug )

  # Inserting standard palettes
  0.upto( 3 ) do |c|
    mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{@cgi['id']}', name='#{@palette_default_name[c]}', palette='#{@palette_default[c]}';", false, @debug )
  end

  # Inserting new history
  mdb( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{@cgi['id']}', his='';", false, @debug )

  # Inserting new SUM
  mdb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{@cgi['id']}', sum='';", false, @debug )

  # Inserting new meal
  mdb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{@cgi['id']}', meal='';", false, @debug )

  # Inserting new config
  mdb( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{@cgi['id']}', his_max=200, recipel='1:0:99:99:99:99:99', koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t';", false, @debug )

  html_regist_finish( lp )

#### Input form
else
  html_regist_form( nil, nil, nil, nil, nil, lp )
end

html_foot()
