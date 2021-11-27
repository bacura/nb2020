# Ginmi module for basal metabolism of athlete 0.00
#encoding: utf-8

@debug = false

off =		%w(1.75 1.75 1.75 1.75 1.50)
training =	%w(2.00 2.00 2.00 2.00 1.75)
game =		%w(2.00 2.00 2.00 2.00 1.75)
@pal_set =	[off, training, game]


def ginmi_module( cgi, user )
	l = module_lp( user.language )
	module_js()

	command = cgi['command']
	html = ''

	case command
	when 'form'
		#importing from config
		weight = 0.0
		body_fat = 10.0
		kexow = 0
		r = mdb( "SELECT bio FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
		if r.first
			if r.first['bio'] != nil && r.first['bio'] != ''
				bio = JSON.parse( r.first['bio'] )
				weight = bio['weight'].to_f
				kexow = bio['kexow'].to_i
			end
		end

		# importing from koyomiex
		if kexow == 1
			kex_select = Hash.new
			r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
			if r.first
				if r.first['koyomi'] != nil && r.first['koyomi'] != ''
					koyomi = JSON.parse( r.first['koyomi'] )
					kex_select = koyomi['kex_select']
				end
			end

			kex_select.each do |k, v|
				if v == 5
					rr = mdb( "SELECT item#{k} FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND item#{k}!='' ORDER BY date DESC LIMIT 1;", false, @debug )
					body_fat = rr.first["item#{k}"].to_f if rr.first
				end

				if v == 3
					rr = mdb( "SELECT item#{k} FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND item#{k}!='' ORDER BY date DESC LIMIT 1;", false, @debug )
					weight = rr.first["item#{k}"].to_f if rr.first
				end
			end
		end


html = <<-"HTML"
		<div class='row'>
		<h5>基礎代謝量 計算フォーム（アスリートの式）</h5>
		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>体重(kg)</span>
					<input type='text' class='form-control' id='weight' maxlength='6' value='#{weight}'>
				</div>
			</div>

			<div class='col-2'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>体脂肪率(%)</span>
					<input type='text' class='form-control' id='body_fat' maxlength='6' value='#{body_fat}'>
				</div>
			</div>

			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">期間</label>
					<select class="form-select form-select-sm" id="period">
						<option value='0'>オフ</option>
						<option value='1' SELECTED>トレーニング</option>
						<option value='2'>試合</option>
					</select>
				</div>
			</div>

			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">種目</label>
					<select class="form-select form-select-sm" id="event">
						<option value='0'>持久系</option>
						<option value='1'>筋力系</option>
						<option value='2'>瞬発系</option>
						<option value='3'>球技系</option>
						<option value='4'>その他</option>
					</select>
				</div>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="ginmiEnergyAthres()">計算</button>
			</div>
		</div>
HTML
	when 'result'
		weight = BigDecimal( cgi['weight'] )
		body_fat = BigDecimal( cgi['body_fat'] )
		period = cgi['period'].to_i
		event = cgi['event'].to_i
		if @debug
			puts "weight:#{weight}<br>\n"
			puts "body_fat:#{body_fat}<br>\n"
			puts "period:#{period}<br>\n"
			puts "event:#{event}<br>\n"
			puts "<hr>\n"
		end

		lean_body_mass = ( weight - ( weight * body_fat / 100 )).round( 1 )
		lean_body_mass_formula = "#{weight.to_f} - ( #{weight.to_f} * #{body_fat.to_f} / 100 )"

		pal = BigDecimal( @pal_set[period][event] )

		result = 0
		formula = ''

		result = 28.5 * lean_body_mass
		formula = "28.5 * #{lean_body_mass.to_f}"

		eer_result = ( result * pal ).round( 0 )
		eer_formula = "#{result.to_i} * #{pal.to_f}"

html = <<-"HTML"
		<div class='row'>
			<div class='col-3'>除脂肪体重(kg)</div>
			<div class='col-2'>#{lean_body_mass.to_f}</div>
			<div class='col-1'>計算式</div>
			<div class='col-6'>#{lean_body_mass_formula}</div>
		</div>
		<br>
		<div class='row'>
			<div class='col-3'>基礎代謝量(kcal/day)</div>
			<div class='col-2'>#{result.to_i}</div>
			<div class='col-1'>計算式</div>
			<div class='col-6'>#{formula}</div>
		</div>
		<br>
		<div class='row'>
			<div class='col-3'>活動係数</div>
			<div class='col-2'>#{pal.to_f}</div>
		</div>
		<br>
		<div class='row'>
			<div class='col-3'>推定エネルギー必要量(kcal/day)</div>
			<div class='col-2'>#{eer_result.to_i}</div>
			<div class='col-1'>計算式</div>
			<div class='col-6'>#{eer_formula}</div>
		</div>
		<hr>
		参考：スポーツ選手の栄養調査・サポート基準値策定及び評価に関するプロジェクト (2006)
HTML
	when 'save'

	end

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var ginmiEnergyAthres = function(){
	var weight = document.getElementById( "weight" ).value;
	var body_fat = document.getElementById( "body_fat" ).value;
	var period = document.getElementById( "period" ).value;
	var event = document.getElementById( "event" ).value;
	$.post( "ginmi.cgi", { mod:"energy-ath", command:'result', weight:weight, body_fat:body_fat, period:period, event:event }, function( data ){ $( "#L2" ).html( data );});
	document.getElementById( "L2" ).style.display = 'block';
};

</script>
JS
	puts js
end

def module_lp( language )
	l = Hash.new
	l['jp'] = {
		'title' => "BMI 計算フォーム",\
		'age' => "年齢",\
		'height' => "身長(m)",\
		'weight' => "体重(kg)",\
		'calc' => "計算"
	}

	return l[language]
end
