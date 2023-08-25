#!/usr/bin/perl --

use utf8;
use open ":utf8";
my $e;

loadForm();        #フォームデータ取り込み

$e = $FORM{'error'};

if($e == 1){$MSG = "コンピュータが思考停止しました...";}
elsif($e == 2){$MSG = "棋譜データが不正です";}
elsif($e == 3){$MSG = "棋譜データが不正です(盤面の高さを越えてコマを置こうとしました)";}
else{$MSG = "";}

printData();        #HTML出力

exit;

#====================================================================HTML出力
sub    printData
{

    print qq(Content-type: text/html; charset=UTF-8\n\n);

    print <<"    END";
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
        <html>
        <head>
        <title>重力付き四目並べ -エラー-</title>
        <style type="text/css">
        <!--
            .msg    { padding:3px; color: #000; font-size:25px; font-weight:bold; text-align:center }
            a       { text-decoration:none;}
            a:hover { text-decoration:underline;}
        //-->
        </style>
        </head>
        <body>
        <center>
        <font size="6"><b>重力付き四目並べ</b></font>
        <hr>
        <font size="4"><b>Error:$e<br>
        $MSG<br><br>
        </b></font>
        <font size="5"><b><a href="./index.cgi">TOP</a></b></font>
        </body>
        </html>
    END
}

#====================================================================フォームデータ取り込み
sub    loadForm
{
    my    ($query, $pair);
    if($ENV{'REQUEST_METHOD'} eq 'POST') {
        read(STDIN, $query, $ENV{'CONTENT_LENGTH'});
    }
    else {
        $query = $ENV{'QUERY_STRING'};
    }
    foreach $pair (split(/&/, $query)) {
        my    ($key, $value) = split(/=/, $pair);
        $value =~ tr/+/ /;
        $value =~ s/%([0-9a-fA-F][0-9a-fA-F])/chr(hex($1))/eg;
        $FORM{$key} = $value;
    }
}