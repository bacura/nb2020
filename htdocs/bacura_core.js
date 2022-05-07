//Javascript for Bacura KYOTO Lab
//bacura_bs3.js ver 0.00


//GitHubのボタン処理
function github_on(){
	document.getElementById( "github" ).src = "img/GitHub-Mark-32px.png";
}

function github_off(){
	document.getElementById( "github" ).src = "img/GitHub-Mark-Light-32px.png";
}

//内容ON-OFFボタン処理
function off_button(){
	var header = document.getElementById( 'header' );
	var nav = document.getElementById( 'nav' );
	var article = document.getElementById( 'article' );
	header.innerHTML = '<span onclick="on_button();">On&nbsp;</span>';
	nav.style.opacity = '0.00';
	article.style.opacity = '0.00';
}

function on_button(){
	var header = document.getElementById( 'header' );
	var nav = document.getElementById( 'nav' );
	var artivle = document.getElementById( 'article' );
	header.innerHTML = '<span onclick="off_button();">Off&nbsp;</span>';
	nav.style.opacity = '1.00';
	article.style.opacity = '1.00';
}

//内容レイヤーの切り替え
//function change_cl( html ){
//	$( "#article" ).load( html );
//}

var sumaho = false;
var sumaho_ = false;

// ci initialization
window.onload = function(){
	var width = $( window ).width();
	var height = $( window ).height();

	$.get( "ci.cgi", { width:width, height:height, img_id:'iid0' }, function( data ){
		$( "#ci0" ).html( data );
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid1' }, function( data ){ $( "#ci1" ).html( data );});
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid2' }, function( data ){ $( "#ci2" ).html( data );});
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid3' }, function( data ){ $( "#ci3" ).html( data );});
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid4' }, function( data ){ $( "#ci4" ).html( data );});
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid5' }, function( data ){ $( "#ci5" ).html( data );});
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid6' }, function( data ){ $( "#ci6" ).html( data );});
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid7' }, function( data ){ $( "#ci7" ).html( data );});
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid8' }, function( data ){ $( "#ci8" ).html( data );});
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid9' }, function( data ){ $( "#ci9" ).html( data );});
	});
}

// ci resize
$( window ).resize( function( event ){
	var width = $( window ).width();
	var height = $( window ).height();

	if( width < height){ sumaho = true; }else{ sumaho = false; }
	if( sumaho_ != sumaho ){
		$.get( "ci.cgi", { width:width, height:height, img_id:'iid0' }, function( data ){
			$( "#ci0" ).html( data );
			$.get( "ci.cgi", { width:width, height:height, img_id:'iid1' }, function( data ){ $( "#ci1" ).html( data );});
			$.get( "ci.cgi", { width:width, height:height, img_id:'iid2' }, function( data ){ $( "#ci2" ).html( data );});
			$.get( "ci.cgi", { width:width, height:height, img_id:'iid3' }, function( data ){ $( "#ci3" ).html( data );});
			$.get( "ci.cgi", { width:width, height:height, img_id:'iid4' }, function( data ){ $( "#ci4" ).html( data );});
			$.get( "ci.cgi", { width:width, height:height, img_id:'iid5' }, function( data ){ $( "#ci5" ).html( data );});
			$.get( "ci.cgi", { width:width, height:height, img_id:'iid6' }, function( data ){ $( "#ci6" ).html( data );});
			$.get( "ci.cgi", { width:width, height:height, img_id:'iid7' }, function( data ){ $( "#ci7" ).html( data );});
			$.get( "ci.cgi", { width:width, height:height, img_id:'iid8' }, function( data ){ $( "#ci8" ).html( data );});
			$.get( "ci.cgi", { width:width, height:height, img_id:'iid9' }, function( data ){ $( "#ci9" ).html( data );});
		});
		sumaho_ = sumaho;
	}

});
