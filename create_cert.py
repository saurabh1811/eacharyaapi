newtext='''<!DOCTYPE html>
<html>
<head>
<style>
	
	.table-inline {
       display: inline-block;
       vertical-align: top;
       margin-right: 5px;
       margin-left: 10px;
     }


   @import url('https://fonts.googleapis.com/css?family=Lato:300,300i,400,400i,700,900');
   
	body{
     font-family: 'Lato', sans-serif;
   }
   .comp_logo {
       height: 50px;
       width: 50px;
       padding-right: 20px;
   }

   .comp_signature {
       height: 70px;
       width: 100px;
       padding-right: 20px;
   }
   .tax-invoice{
     width:920px;
     margin:0 auto;
     margin-top:80px;
     padding-top:20px
   }
   .text-center{
     text-align:center;
   }
   .text-left{
     text-align:left;
   }
   .text-right{
     text-align:right;
   }
  
   .block{
     display:block;
     margin-top: 8px;
   }

   .block1
   {
     margin-top: 100px ! important;
   }
   .des-table td, .des-table th{
     border-right:solid 1px #000;
     border-bottom:solid 1px #000;
   }
   .des-table td.height100{
     height:200px;
   }
   .des-table th{
     padding:12px 5px;
     font-size:14px;
   }
   .border-bottom{
     border-bottom:solid 1px #000;
   }
   .border-top{
     border-top:solid 1px #000;
   }
   .border-right{
     border-right:solid 1px #000;
   }
   .border-left{
     border-left:solid 1px #000;
   }
   .des-table td{
     padding:5px;
   }
   .width50{
     width:50%%;
   }
   .font13{
     font-size:13px;
   }
   .font14{
     font-size:14px;
   }
   .font15{
     font-size:15px;
   }
   .font16{
     font-size:16px;
   }
   .bold{
     font-weight:900;
   }
   .semi-bold{
     font-weight:700;
   }
   .no-right-border{
     border-right:none !important;
   }
   .no-bottom-border{
     border-bottom:none !important;
   }
   .top{
     vertical-align:top;
   }
   .top20{
     margin-top:20px;
   }
   .no-margin{
     margin:0px;
   }
   .terms{
     list-style:none;
     margin:0px;
     padding:0px;
   }
   .space{
     display: inline-block;
       width: 30px;
       text-align: center;
   }
   .underline{
     text-decoration:underline;
   }
   .company-name{
     font-size: 20px;
       font-weight: 600;
     line-height:34px !important;
   }
   .header-table td{
     line-height:20px;
   }
   .address-table td{
       padding: 8px 20px;
   }
   .padding-btm10{
     padding-bottom:10px;
   }
   .width120px{
     display: inline-block;
 
   }
   .top70{
     margin-top:70px;
   }
   .padding-top10{
     padding-top:10px;
   }
   .terms li{
     font-size:14px;
     line-height:19px;
   }
   .footer td{
   }

   
   .receiver{
     padding-top:10px;
     padding-bottom:20px;
     padding-left:5px;
   }
   .pad5{
     padding-left:5px;
   }
   .border-right-none{
     border-right:none !important;
   }
   .padr10{
     padding-right:10px;
   }

   .space2{
     display: inline-block;
    width: 50px;
    text-align: center;
  }
  .width80px{
     width:80px;
  }
  .width150px{
     width:150px;
     display:inline-block
  }
  .width200px{
     width:200px;
     display:inline-block
  }
  .width250px{
     width:250px;
     display:inline-block
  }
  .width100px{
     width:100px;
     display:inline-block
  }
  .height19{
     height:19px;
     display:block;
  }
  .rupees-align{
   display: inline-block;
  }

  .new_gst td {
   padding: 2px 0px 2px 15px;
   font-size: 14px;
   text-align: right;
  }
  .new_gst .first_row td {
   font-weight: 700;
   border-bottom: 1px solid black;
  }
  .empty_span{
     height: 15px;
     display: block;
  }

  .spc
  {
  margin-left: 123px;
  }
  .spc1
  {
   margin-left: 150px;
  }


  th, td {
   padding: 5px;
  }
  th {
   text-align: left;
  }
  .space1
  {
  margin-left: 40px ! important;
  }

  .margin1
  {
   margin-left: 20px ! important;
  }

  .spcdot
  {
  margin-left: 34px;
  }
  .spcdotuhid
  {
  margin-left: 23px;
  }

  .spcdotadd
  {
  margin-left: 4px;
  }

  .spcemail
  {
  margin-left: -5px;
  }
  .spcsex
  {
     margin-left: 21px;
  }

  .spcphone
  {
  margin-left: -7px;
  }
  .spcname
  {
  padding-left: 21px;

  }
  .discharge
  {
  margin-left: 18px;
  }
  .bed
  {
  margin-left: 123px;
  }
  .spcdia
  {
  margin-bottom: 9px;
  }

  .sze
  {
  height: 450px;
  }
  .clinicalnar
  {
  margin-bottom: 15px;
  }

  .text-right
  {
   text-align:right;
  }
  .text-left
  {
   text-align:left;

  }
</style>

  <title></title>
</head>
<body>
  <div class="tax-invoice" >
    <table cellpadding="0" cellspacing="0" class="border-bottom header-table padding-btm10" width="100%%">
      <tr>
        <td class="text-center company-name">Certificate of Completion<br></td>
      </tr>
      <tr>
        <td class="text-center">This is to certify that<br></td>
      </tr>
      <tr>
        <td class="text-center">%s<br></td>
      </tr>
      <tr>
        <td class="text-center">from<br></td>
      </tr>
      <tr>
        <td class="text-center">%s<br></td>
      </tr>
      <tr>
        <td class="text-center">attended as a Distingjished Speaker at<br></td>
      </tr>
      <tr>
        <td class="text-center">Sri Lanka Hospitality<br></td>
      </tr>
      <tr>
        <td class="text-center">Investment Conference<br></td>
      </tr>
      <tr>
        <td class="text-center">held on<br></td>
      </tr>
      <tr>
        <td class="text-center">%s<br></td>
      </tr>
      <tr>
        <td class="text-center">at<br></td>
      </tr>
      <tr>
        <td class="text-center">Cinnamon Lakeside | Sri Lanka<br></td>
      </tr>
      <tr>
        <td></td>
      </tr>
      <tr>
        <td class="text-right"><img alt="Smiley face" height="80" src="images/sign.png" width="150"></td>
      </tr>
      <tr>
        <td class="text-left"><img alt="Smiley face" height="80" src="images/sign.png" style="margin-top: -141px ! important;" width="150"></td>
      </tr>
    </table>
  </div>
</body>
</html>'''