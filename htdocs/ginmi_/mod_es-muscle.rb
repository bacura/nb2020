# Ginmi module for Estimated muscle 0.00
#encoding: utf-8

def ginmi_module( cgi, user )
	module_js()

	command = cgi['command']
	html = ''

	case command
	when 'form'
		ac = 0.0
		tsf = 0.0

html = <<-"HTML"
		<div class='row'>
		<h5>上腕筋面積 計算フォーム</h5>
		</div>
		<br>

		<div class='row'>
			<div class='col-3'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>上腕周囲長(cm)</span>
					<input type='text' class='form-control' id='ac' maxlength='6' value='#{ac}'>
				</div>
			</div>

			<div class='col-4'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>上腕三頭筋皮下脂肪厚(cm)</span>
					<input type='text' class='form-control' id='tsf' maxlength='6' value='#{tsf}'>
				</div>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="ginmiEsMuscleres()">計算</button>
			</div>
		</div>
HTML
	when 'result'
		ac = BigDecimal( cgi['ac'] )
		tsf = BigDecimal( cgi['tsf'] )
		if @debug
			puts "ac:#{ac}<br>\n"
			puts "tsft:#{tsf}<br>\n"
			puts "<hr>\n"
		end
		result = (( ac - Math::PI * tsf / 10)**2 / ( 4 * Math::PI )).round( 1 )

html = <<-"HTML"
		<div class='row'>
			<div class='col-2'>上腕筋面積(cm^2)</div>
			<div class='col-2'>#{result.to_f}</div>
			<div class='col-2'>計算式</div>
			<div class='col-6'>( #{ac.to_f} - pi * #{tsf.to_f} / 10 )^2 / ( 4 * pi )</div>
		</div>
		<br>
HTML
	when 'save'

	end

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var ginmiEsMuscleres = function(){
	var ac = document.getElementById( "ac" ).value;
	var tsf = document.getElementById( "tsf" ).value;
	$.post( "ginmi.cgi", { mod:"es-muscle", command:'result', ac:ac, tsf:tsf }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};

</script>
JS
	puts js
end
