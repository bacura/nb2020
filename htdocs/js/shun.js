/////////////////////////////////////////////////////////////////////////////////
// Cooking school //////////////////////////////////////////////////////////////

//
var initSchool = function(){
	closeBroseWindows( 1 );
	$.post( "school.cgi", { command:"menu" }, function( data ){ $( "#LINE" ).html( data );});
	$.post( "school.cgi", { command:"init" }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
	displayLINE( 'on' );
};

// School koyomi change
var changeSchoolk = function(){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( "school.cgi", { command:"init", yyyy_mm:yyyy_mm }, function( data ){ $( "#L1" ).html( data );});
};

// School status change
var changeSchoolkSt = function( dd, ampm, status ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( "school.cgi", { command:"changest", yyyy_mm:yyyy_mm, dd:dd, ampm:ampm, status:status }, function( data ){ $( "#L1" ).html( data );});
};

// School open
var openSchoolk = function( dd, ampm ){
	var yyyy_mm = document.getElementById( "yyyy_mm" ).value;
	$.post( "school.cgi", { command:"open", yyyy_mm:yyyy_mm, dd:dd, ampm:ampm }, function( data ){ $( "#L1" ).html( data );});
};

/////////////////////////////////////////////////////////////////////////////////
// Cooking school menu //////////////////////////////////////////////////////////////

// menu
var initSchoolMenu = function(){
	closeBroseWindows( 1 );
	document.getElementById( "L1" ).style.display = 'block';
	$.post( "school-menu.cgi", { command:"init" }, function( data ){ $( "#L1" ).html( data );});
	displayLINE( 'on' );
};


// Making new school menu tag group
var mekeSchoolGroup = function(){
	var group_new = document.getElementById( 'group_new' ).value;
	$.post( "school-menu.cgi", { command:"group_new", group_new:group_new }, function( data ){ $( "#L1" ).html( data );});
};

// Changing school menu tag name
var changeSchoolTagName = function( tag_group, group_no, tag_no ){
	var tag_name_new = document.getElementById( 'tag_name' + group_no + '_' + tag_no ).value;
	$.post( "school-menu.cgi", { command:"tag_name_change", tag_group:tag_group, tag_no:tag_no, tag_name_new:tag_name_new }, function( data ){ $( "#L1" ).html( data );});
	displayVIDEO( tag_name_new );
};

// Changing school menu tag
var changeSchoolTag = function( tag_group, group_no, tag_no ){
	var tag_new = document.getElementById( 'tag' + group_no + '_' + tag_no ).value;
	$.post( "school-menu.cgi", { command:"tag_change", tag_group:tag_group, tag_no:tag_no, tag_new:tag_new }, function( data ){ $( "#L1" ).html( data );});
	displayVIDEO( tag_new );
};


/////////////////////////////////////////////////////////////////////////////////
// Cooking school stock //////////////////////////////////////////////////////////////

// menu
var initSchoolStock = function(){
	closeBroseWindows( 1 );
	$.post( "school-stock.cgi", { command:"init" }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Management of account M //////////////////////////////////////////////////////////////

// Account list
var initAccountM = function(){
	closeBroseWindows( 1 );
	$.post( "account-mom.cgi", { command:"init" }, function( data ){ $( "#L1" ).html( data );});
	document.getElementById( "L1" ).style.display = 'block';
};


// New account form
var newAccountM = function(){
	$.post( "account-mom.cgi", { command:"new" }, function( data ){ $( "#L1" ).html( data );});
};


// Save new account
var saveAccountM = function(){
	var uid_d = document.getElementById( 'uid_d' ).value;
	var mail_d = document.getElementById( 'mail_d' ).value;
	var pass_d = document.getElementById( 'pass_d' ).value;
	var aliasu_d = document.getElementById( 'aliasu_d' ).value;
	var language_d = document.getElementById( 'language_d' ).value;
	$.post( "account-mom.cgi", { command:"save", uid_d:uid_d, mail_d:mail_d, pass_d:pass_d, aliasu_d:aliasu_d, language_d:language_d }, function( data ){ $( "#L1" ).html( data );});
};


// Update account
var updateAccountM = function( uid_d ){
	var mail_d = document.getElementById( 'mail_d' ).value;
	var pass_d = document.getElementById( 'pass_d' ).value;
	var aliasu_d = document.getElementById( 'aliasu_d' ).value;
	var language_d = document.getElementById( 'language_d' ).value;
	$.post( "account-mom.cgi", { command:"update", uid_d:uid_d, mail_d:mail_d, pass_d:pass_d, aliasu_d:aliasu_d, language_d:language_d }, function( data ){ $( "#L1" ).html( data );});
};


// Edit account
var editAccountM = function( uid_d ){
	$.post( "account-mom.cgi", { command:"edit", uid_d:uid_d }, function( data ){ $( "#L1" ).html( data );});
};


// Delete account
var deleteAccountM = function( uid_d ){
	if(document.getElementById( "delete_checkM" ).checked){
		$.post( "account-mom.cgi", { command:"delete", uid_d:uid_d }, function( data ){ $( "#L1" ).html( data );});
	}else{
		displayVideo( 'Check! (>_<)' );
	}
};


// Switch account
var switchAccountM = function( switch_id, uid_d ){
	if(document.getElementById( switch_id ).checked){ var switch_d = 1; }else{ var switch_d = 0; }
	$.post( "account-mom.cgi", { command:"switch", uid_d:uid_d, switch_d:switch_d }, function( data ){});
};
