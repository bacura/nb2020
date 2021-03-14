#! /usr/bin/ruby
# coding: utf-8
#Nutrition browser 2020 index page 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '../nb2020-soul'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'index'


#==============================================================================
#DEFINITION
#==============================================================================

#### HTML top
def html_top( user, lp )
  user_name = user.name
  user_name = user.aliasu if user.aliasu != '' && user.aliasu != nil
  uid = user.uid
  mid = user.mid

  case user.status
  when 1
    login_color = "primary"
  when 3, 6
    login_color = "warning"
  when 2, 4
    login_color = "info"
  when 5
    login_color = "success"
  when 8, 9
    login_color = "danger"
  else
    login_color = "secondary"
  end

  mom = ''
  mom_a = ''
  daughters = []
  daughters_a = []
  mom_flag = false

  if user.mom == user.name
    r = mdb( "SELECT * FROM user WHERE mom='#{user.name}' AND status='6';", false, false )
    r.each do |e|
      if e['switch'] == 1
        daughters << e['user']
        daughters_a << e['aliasu'].to_s
      end
    end
    mom = user.name
    mom_a = user.aliasu
  else
    r = mdb( "SELECT * FROM user WHERE user='#{user.mom}';", false, false )
    if r.first
      if r.first['cookie_m'] == mid
        mom = r.first['user']
        mom_a = r.first['aliasu']
        mom_a = mom if mom_a == ''

        rr = mdb( "SELECT * FROM user WHERE mom='#{mom}' AND status='6';", false, false )
        rr.each do |e|
          if e['switch'] == 1
            daughters << e['user']
            daughters_a << e['aliasu'].to_s
          end
        end
      end
    end
  end

  login = ''
  if daughters.size > 0 || mom_flag
    login = "<div class='form-inline'>"
    login << "<SELECT style='background-color:#343a40' id='login_mv' class='custom-select text-#{login_color}' onchange=\"chageAccountM( '#{mid}' )\">"
    login << "<OPTION value='#{mom}'>#{mom_a}</OPTION>"
    daughters.size.times do |c|
      t = daughters[c]
      t = daughters_a[c] unless daughters_a[c] == ''
      if daughters[c] == user.name
        login << "<OPTION value='#{daughters[c]}' SELECTED>#{t}</OPTION>"
      else
        login << "<OPTION value='#{daughters[c]}'>#{t}</OPTION>"
      end
    end
    login << "</SELECT>"
    login << "&nbsp;#{lp[56]}&nbsp;|&nbsp;<a href=\"login.cgi?mode=logout\" class=\"text-#{login_color}\">#{lp[55]}</a>"
    login << "</div>"
  else
    login = "#{user_name}&nbsp;さん&nbsp;|&nbsp;<a href=\"login.cgi?mode=logout\" class=\"text-#{login_color}\">#{lp[55]}</a>"
  end
  login = "<a href='login.cgi' class=\"text-#{login_color}\">#{lp[60]}</a>&nbsp;|&nbsp;<a href=\"regist.cgi\" class=\"text-#{login_color}\">#{lp[53]}</a>" if user_name == nil

  html = <<-"HTML"
      <header class="navbar navbar-expand-lg navbar-dark bg-dark" id="header">
        <div class="container-fluid">
          <a href="index.cgi" class="navbar-brand h1 text-#{login_color}">#{lp[54]}</a>
          <span class="navbar-text text-#{login_color} login_msg h4">#{login}</span>
          <a href='https://neg.bacura.jp/?page_id=1154' target='manual'>#{lp[51]}</a>
          <span class="d-flex">
            <select class="form-select" id="qcate">
              <option value='0'>#{lp[57]}</option>
              <option value='1'>#{lp[58]}</option>
              <option value='2'>#{lp[59]}</option>
            </select>
            <input class="form-control" type="text" maxlength="100" id="words" onchange="search()">
            <btton class='btn btn-sm' onclick="search()">#{lp[52]}</button>
          </span>
        </div>
      </header>
HTML

  puts html
end

#### HTML nav
def html_nav( user, lp )
  cb_num = ''
  meal_num = ''
  # まな板カウンター
  if user.name
    r = mdb( "SELECT sum from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
    if r.first
      t = []
      t = r.first['sum'].split( "\t" ) if r.first['sum']
      cb_num = t.size
    else
      mdb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{user.name}';", false, @debug )
      cb_num = 0
    end
    # 献立カウンター
    r = mdb( "SELECT meal from #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';", false, @debug )
    if r.first
      t = []
      t = r.first['meal'].split( "\t" ) if r.first['meal']
      meal_num = t.size
    else
      mdb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{user.name}';", false, @debug )
      meal_num = 0
    end
  else
    cb_num = '-'
    meal_num = '-'
  end

  # 履歴ボタンとまな板ボタンの設定
  if user.status >= 1
    cb = "#{lp[1]} <span class=\"badge rounded-pill bg-dark text-light\" id=\"CBN\">#{cb_num}</span>"
    mb = "#{lp[2]} <span class=\"badge rounded-pill bg-dark text-light\" id=\"MBN\">#{meal_num}</span>"
    special_button = "<button type=\"button\" class=\"btn btn-outline-dark btn-sm nav_button\" id=\"category0\" onclick=\"summonL1( 0 )\">#{@category[0]}</button>"
    his_button = "<button type=\"button\" class=\"btn btn-primary btn-sm nav_button\" onclick=\"historyInit()\">#{lp[4]}</button>"
    sum_button = "<button type='button' class='btn btn-outline-dark btn-sm nav_button' onclick=\"initCB( '' )\">#{cb}</button>"
    recipe_button = "<button type='button' class='btn btn-outline-dark btn-sm nav_button' onclick=\"recipeList( 'init' )\">#{lp[5]}</button>"
    menu_button = "<button type='button' class='btn btn-outline-dark btn-sm nav_button' onclick=\"initMeal( '' )\">#{mb}</button>"
    set_button = "<button type='button' class='btn btn-outline-dark btn-sm nav_button' onclick=\"menuList()\">#{lp[6]}</button>"
    config_button = "<button type='button' class='btn btn-outline-dark btn-sm nav_button' onclick=\"configInit( '' )\">#{lp[7]}</button>"
  else
    cb = "#{lp[1]} <span class=\"badge badge-pill badge-secondary\" id=\"CBN\">#{cb_num}</span>"
    mb = "#{lp[2]} <span class=\"badge badge-pill badge-secondary\" id=\"MBN\">#{meal_num}</span>"
    special_button = "<button type=\"button\" class=\"btn btn-outline-secondary btn-sm nav_button\" onclick=\"displayVideo( '#{lp[8]}' )\">#{@category[0]}</button>"
    his_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[4]}</button>"
    sum_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{cb}</button>"
    recipe_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[5]}</button>"
    menu_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{mb}</button>"
    set_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[6]}</button>"
    config_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[7]}</button>"
  end

  if user.status >= 3
    g_button = "<button type='button' class='btn btn btn-warning btn-sm nav_button text-warning guild_color' onclick=\"changeMenu( '#{user.status}' )\">G</button>"
  else
    g_button = "<button type='button' class='btn btn btn-warning btn-sm nav_button text-dark guild_color' onclick=\"displayVideo( '#{lp[9]}' )\">G</button>"
  end

  gm_account = ''
  if user.status == 9
    gm_account << "<button type='button' class='btn btn-warning btn-sm nav_button text-warning guild_color' onclick=\"initAccount( 'init' )\">#{lp[34]}</button>"
    gm_account << "<button type='button' class='btn btn-warning btn-sm nav_button text-warning guild_color' onclick=\"initExport( 'init' )\">#{lp[3]}</button>"
    gm_account << "<button type='button' class='btn btn-warning btn-sm nav_button text-warning guild_color' onclick=\"initImport( 'init' )\">#{lp[38]}</button>"
  end

  html = <<-"HTML"
      <nav class='container-fluid'>
          #{g_button}
          <button type="button" class="btn btn-info btn-sm nav_button" id="category1" onclick="summonL1( 1 )">#{@category[1]}</button>
          <button type="button" class="btn btn-info btn-sm nav_button" id="category2" onclick="summonL1( 2 )">#{@category[2]}</button>
          <button type="button" class="btn btn-info btn-sm nav_button" id="category3" onclick="summonL1( 3 )">#{@category[3]}</button>
          <button type="button" class="btn btn-danger btn-sm nav_button" id="category4" onclick="summonL1( 4 )">#{@category[4]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button" id="category5" onclick="summonL1( 5 )">#{@category[5]}</button>
          <button type="button" class="btn btn-success btn-sm nav_button" id="category6" onclick="summonL1( 6 )">#{@category[6]}</button>
          <button type="button" class="btn btn-info btn-sm nav_button" id="category7" onclick="summonL1( 7 )">#{@category[7]}</button>
          <button type="button" class="btn btn-success btn-sm nav_button" id="category8" onclick="summonL1( 8 )">#{@category[8]}</button>
          <button type="button" class="btn btn-success btn-sm nav_button" id="category9" onclick="summonL1( 9 )">#{@category[9]}</button>
          <button type="button" class="btn btn-danger btn-sm nav_button" id="category10" onclick="summonL1( 10 )">#{@category[10]}</button>
          <button type="button" class="btn btn-danger btn-sm nav_button" id="category11" onclick="summonL1( 11 )">#{@category[11]}</button>
          <button type="button" class="btn btn-danger btn-sm nav_button" id="category12" onclick="summonL1( 12 )">#{@category[12]}</button>
          <button type="button" class="btn btn-outline-secondary btn-sm nav_button" id="category13" onclick="summonL1( 13 )">#{@category[13]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button" id="category14" onclick="summonL1( 14 )">#{@category[14]}</button>
          <button type="button" class="btn btn-secondary btn-sm nav_button" id="category15" onclick="summonL1( 15 )">#{@category[15]}</button>
          <button type="button" class="btn btn-primary btn-sm nav_button" id="category16" onclick="summonL1( 16 )">#{@category[16]}</button>
          <button type="button" class="btn btn-outline-secondary btn-sm nav_button" id="category17" onclick="summonL1( 17 )">#{@category[17]}</button>
          <button type="button" class="btn btn-secondary btn-sm nav_button" id="category18" onclick="summonL1( 18 )">#{@category[18]}</button>
          #{special_button}
          #{his_button}
          #{sum_button}
          #{recipe_button}
          #{menu_button}
          #{set_button}
          <button type="button" class="btn btn-outline-secondary btn-sm nav_button" onclick="bookOpen( 'books/books.html', 1 )">#{lp[28]}</button>
          #{config_button}
      </nav>
      <nav class='container-fluid' id='guild_menu' style='display:none;'>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initKoyomi()">#{lp[37]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initGinmi()">#{lp[40]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="">#{lp[42]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="">#{lp[43]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="">#{lp[44]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="">#{lp[45]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="">#{lp[46]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initToker()">#{lp[50]}</button>
      </nav>
      </nav>
      <nav class='container-fluid' id='gs_menu' style='display:none;'>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initAccountM()">#{lp[48]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initSchool()">#{lp[47]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="">#{lp[49]}</button>
      </nav>
      <nav class='container-fluid' id='gm_menu' style='display:none;'>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initUnitc( 'init' )">#{lp[29]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initColor( 'init' )">#{lp[30]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initAllergen( 'init' )">#{lp[31]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initGYCV( 'init' )">#{lp[35]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initShun( 'init' )">#{lp[36]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initDic( 'init' )">#{lp[32]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initSlogf( 'init' )">#{lp[33]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initMemory( 'init' )">#{lp[39]}</button>
          #{gm_account}
      </nav>
HTML
  puts html
end


#### HTML working space
def html_working( dummy )
  html = <<-"HTML"
      <div class="bw_frame" id='bw_frame' aligh="center">
        <div class="line" id='LINE' style="display: block;"></div>
        <div class="browse_window" id='L1' style="display: none;"></div>
        <div class="browse_window" id='L2' style="display: none;"></div>
        <div class="browse_window" id='L3' style="display: none;"></div>
        <div class="browse_window" id='L4' style="display: none;"></div>
        <div class="browse_window" id='L5' style="display: none;"></div>
        <div class="browse_window" id='LF' style="display: none;"></div>
        <div class="video" id='VIDEO' style="display: none;"></div>
      </div>
HTML

  puts html
end


#==============================================================================
# Main
#==============================================================================

html_init( nil )
user = User.new( @cgi )
user.status = 0 unless user.name

lp = user.load_lp( script )

r = mdb( "SELECT ifix FROM cfg WHERE user='#{user.name}';", false, @debug )
ifix = r.first['ifix'].to_i if r.first

html_head( nil, user.status, nil )

puts "<div style='position:fixed; z-index:100; background-color:white'>" if ifix == 1

html_top( user, lp )
html_nav( user, lp )

if ifix == 1
  puts '</div>'
  puts '<header class="navbar navbar-dark bg-dark"><h4> </h4></header>'
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
end
if user.status >= 3 && ifix == 1
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
end

html_working( nil )

html_foot()
