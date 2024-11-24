from collections import defaultdict
from queries import select_codes_from_lineItem
from shopify_data import retrieve_product_title, retrieve_shopify_data
from utils import get_product_id_by_sku, get_product_name_by_sku




def mail_body(event, connexion, firstName, vendor, productIds, productTitles, skus, line_item_ids):
  

  BODY_HTML = f"""<!DOCTYPE html> 
  <html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
  <head>
    <title> </title>
    <!--[if !mso]><!--> 
    <meta content="IE=edge" http-equiv="X-UA-Compatible"/>
    <!--<![endif]--> 
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    <meta content="width=device-width, initial-scale=1" name="viewport"/>
    <!--[if mso]> 
    <noscript>
      <xml>
        <o:OfficeDocumentSettings>
          <o:AllowPNG/>
          <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
      </xml>
    </noscript>
    <![endif]--> <!--[if lte mso 11]> 
    <style type="text/css" data-inliner="ignore"> .mj-outlook-group-fix {{ width:100% !important; }} </style>
    <![endif]--> <!--[if !mso]><!--><!--<![endif]--> 
    <style>a:link {{color:#6487BA;font-weight:normal;text-decoration:underline;font-style:normal}} a:visited {{color:#6487BA;font-weight:normal;text-decoration:underline;font-style:normal}} a:active {{color:#6487BA;font-weight:normal;text-decoration:underline;font-style:normal}} a:hover {{color:#6487BA;font-weight:normal;text-decoration:underline;font-style:normal}}</style>
    <style>@import url(https://static-forms.klaviyo.com/fonts/api/v1/KQsfB7/custom_fonts.css); #outlook a {{ padding: 0 }} body {{ margin: 0; padding: 0; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100% }} table, td {{ border-collapse: collapse; mso-table-lspace: 0; mso-table-rspace: 0 }} img {{ border: 0; line-height: 100%; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic }} p {{ display: block; margin: 13px 0 }} @media only screen and (min-width: 480px) {{ .mj-column-per-100 {{ width: 100% !important; max-width: 100% }} }} .moz-text-html .mj-column-per-100 {{ width: 100% !important; max-width: 100% }} @media only screen and (max-width: 480px) {{ div.kl-row.colstack div.kl-column {{ display: block !important; width: 100% !important }} }} @media only screen and (max-width: 480px) {{ .kl-text {{ padding-right: 18px !important; padding-left: 18px !important }} }} @media only screen and (max-width: 480px) {{ .component-wrapper .mob-no-spc {{ padding-left: 0 !important; padding-right: 0 !important }} }} @media only screen and (max-width: 480px) {{ td.kl-img-base-auto-width {{ width: 100% !important }} }} .kl-button a {{ display: block !important }} @media only screen and (max-width: 480px) {{ .kl-table-subblock.use-legacy-mobile-padding {{ padding-left: 9px !important; padding-right: 9px !important }} }} img {{ border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; max-width: 100% }} .root-container {{ background-repeat: repeat !important; background-size: auto !important; background-position: left top !important }} .root-container-spacing {{ padding-top: 50px !important; padding-bottom: 20px !important; font-size: 0 !important }} .content-padding {{ padding-left: 0 !important; padding-right: 0 !important }} .content-padding.first {{ padding-top: 0 !important }} .content-padding.last {{ padding-bottom: 0 !important }} @media only screen and (max-width: 480px) {{ td.mobile-only {{ display: table-cell !important }} div.mobile-only {{ display: block !important }} table.mobile-only {{ display: table !important }} .desktop-only {{ display: none !important }} }} @media only screen and (max-width: 480px) {{ .table-mobile-only {{ display: table-cell !important; max-height: none !important }} .table-mobile-only.block {{ display: block !important }} .table-mobile-only.inline-block {{ display: inline-block !important }} .table-desktop-only {{ max-height: 0 !important; display: none !important; mso-hide: all !important; overflow: hidden !important }} }} p {{ margin-left: 0; margin-right: 0; margin-top: 0; margin-bottom: 0; padding-bottom: 1em }} @media only screen and (max-width: 480px) {{ .kl-text > div, .kl-table-subblock div, .kl-split-subblock > div {{ font-size: 14px !important; line-height: 1.3 !important }} }} h1 {{ color: #002961; font-family: "Work Sans", Arial, "Helvetica Neue", Helvetica, sans-serif; font-size: 35px; font-style: Normal; font-weight: 800; line-height: 1.1; letter-spacing: 0; margin: 0; margin-bottom: 10px; text-align: center }} @media only screen and (max-width: 480px) {{ h1 {{ font-size: 27px !important; line-height: 1.1 !important }} }} h2 {{ color: #002961; font-family: "Work Sans", Arial, "Helvetica Neue", Helvetica, sans-serif; font-size: 27px; font-style: Normal; font-weight: 800; line-height: 1.1; letter-spacing: 0; margin: 0; margin-bottom: 0; text-align: center }} @media only screen and (max-width: 480px) {{ h2 {{ font-size: 22px !important; line-height: 1.1 !important }} }} h3 {{ color: #002961; font-family: "Work Sans", Arial, "Helvetica Neue", Helvetica, sans-serif; font-size: 20px; font-style: Normal; font-weight: 800; line-height: 1.1; letter-spacing: 0; margin: 0; margin-bottom: 0; text-align: center }} @media only screen and (max-width: 480px) {{ h3 {{ font-size: 17px !important; line-height: 1.1 !important }} }} h4 {{ color: #002961; font-family: "Work Sans", Arial, "Helvetica Neue", Helvetica, sans-serif; font-size: 16px; font-style: Normal; font-weight: 500; line-height: 1.1; letter-spacing: 0; margin: 0; margin-bottom: 0; text-align: center }} @media only screen and (max-width: 480px) {{ h4 {{ font-size: 15px !important; line-height: 1.1 !important }} }} @media only screen and (max-width: 480px) {{ .root-container {{ width: 100% !important }} .root-container-spacing {{ padding: 10px !important }} .content-padding {{ padding-left: 0 !important; padding-right: 0 !important }} .content-padding.first {{ padding-top: 0 !important }} .content-padding.last {{ padding-bottom: 0 !important }} .component-wrapper {{ padding-left: 0 !important; padding-right: 0 !important }} }}</style>
  </head>
  <body style="word-spacing:normal;background-color:#FFFFFF;">
    <div class="root-container" id="bodyTable" style="background-color:#FFFFFF;">
      <div class="root-container-spacing">
        <table align="center" border="0" cellpadding="0" cellspacing="0" class="kl-section" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td>
                <!--[if mso | IE]>
                <table align="center" border="0" cellpadding="0" cellspacing="0" class="kl-section-outlook" style="width:600px;" width="600" >
                  <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                      <![endif]--> 
                      <div style="margin:0px auto;max-width:600px;">
                        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                          <tbody>
                            <tr>
                              <td style="direction:ltr;font-size:0px;padding:0px;text-align:center;">
                                <!--[if mso | IE]>
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                  <table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" bgcolor="#FCF5EE" >
                                    <tr>
                                      <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                                        <![endif]--> 
                                        <div style="background:#FCF5EE;background-color:#FCF5EE;margin:0px auto;border-radius:0px 0px 0px 0px;max-width:600px;">
                                          <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#FCF5EE;background-color:#FCF5EE;width:100%;border-radius:0px 0px 0px 0px;">
                                            <tbody>
                                              <tr>
                                                <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-left:0px;padding-right:0px;padding-top:0px;text-align:center;">
                                                  <!--[if mso | IE]>
                                                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                                    <![endif]--> 
                                                    <div class="content-padding first">
                                                      <!--[if true]>
                                                      <table border="0" cellpadding="0" cellspacing="0" width="600" style="width:600px;direction:ltr">
                                                        <tr>
                                                          <![endif]--> 
                                                          <div class="kl-row" style="display:table;table-layout:fixed;width:100%;">
                                                            <!--[if true]>
                                                            <td style="vertical-align:middle;width:600px;">
                                                              <![endif]--> 
                                                              <div class="kl-column" style="display:table-cell;vertical-align:middle;width:100%;">
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="background-color:#FFFFFF;vertical-align:top;padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:18px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-text" style="font-size:0px;padding:0px;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;word-break:break-word;">
                                                                                  <div style="font-family:'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif;font-size:14px;font-style:Normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;color:#002961;">
                                                                                    <div style="text-align: center;"><span style="color: #6487ba; font-size: 9px;"><em><span class="notion-enable-hover" data-token-index="0">Visualisez {{% web_view '</span><span style="text-decoration: underline;"><span class="notion-enable-hover" data-token-index="1">la version en ligne ici</span></span><span class="notion-enable-hover" data-token-index="2">' %}}</span></em></span></div>
                                                                                  </div>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper desktop-only" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="background-color:#fcf5ee;vertical-align:top;padding-top:9px;padding-right:9px;padding-bottom:0px;padding-left:9px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-image" style="font-size:0px;word-break:break-word;">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                    <tbody>
                                                                                      <tr>
                                                                                        <td class="" style="border:0;padding:0px 9px 0px 9px;background-color:#fcf5ee;width:170px;" valign="top">
                                                                                          <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                            <tbody>
                                                                                              <tr>
                                                                                                <td valign="top"> <img src="https://d3k81ch9hvuctc.cloudfront.net/company/KQsfB7/images/0b25b82c-5a9c-4c5b-8cfe-56ea1b4a5d03.png" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" width="170"/> </td>
                                                                                              </tr>
                                                                                            </tbody>
                                                                                          </table>
                                                                                        </td>
                                                                                      </tr>
                                                                                    </tbody>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <!--[if !mso]><!-->
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper mobile-only" style="display:none; font-size:0; text-align:left; direction:ltr; vertical-align:top; width:100%">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="background-color:#fcf5ee;vertical-align:top;padding-top:9px;padding-right:9px;padding-bottom:8px;padding-left:9px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-image" style="font-size:0px;word-break:break-word;">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                    <tbody>
                                                                                      <tr>
                                                                                        <td class="" style="border:0;padding:0px 9px 0px 9px;width:130px;" valign="top">
                                                                                          <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                            <tbody>
                                                                                              <tr>
                                                                                                <td valign="top"><img src="https://d3k81ch9hvuctc.cloudfront.net/company/KQsfB7/images/0b25b82c-5a9c-4c5b-8cfe-56ea1b4a5d03.png" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" width="130"/></td>
                                                                                              </tr>
                                                                                            </tbody>
                                                                                          </table>
                                                                                        </td>
                                                                                      </tr>
                                                                                    </tbody>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <!--<![endif]--> 
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="vertical-align:top;padding-top:9px;padding-right:0px;padding-bottom:9px;padding-left:0px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="left" class="kl-image" style="font-size:0px;word-break:break-word;">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                    <tbody>
                                                                                      <tr>
                                                                                        <td class="kl-img-base-auto-width" style="border:0;padding:0px 0px 0px 0px;width:600px;" valign="top"> <a href="https://thebradery.com/" style="color:#6487BA; font-style:normal; font-weight:normal; text-decoration:underline"> <img src="https://d3k81ch9hvuctc.cloudfront.net/company/KQsfB7/images/679e4bc5-b9d3-46c4-82f9-7b3f3ff3422e.gif" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" width="600"/> </a> </td>
                                                                                      </tr>
                                                                                    </tbody>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="mob-no-spc" style="vertical-align:top;padding-top:10px;padding-right:75px;padding-bottom:0px;padding-left:75px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-text" style="font-size:0px;padding:0px;padding-top:0px;padding-right:10px;padding-bottom:0px;padding-left:10px;word-break:break-word;">
                                                                                  <div style="font-family:'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif;font-size:14px;font-style:Normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;color:#002961;">
                                                                                    <h3>Hello {firstName}!<span style="font-size: 16px; color: rgb(157, 157, 157);"><br/></span></h3>
                                                                                  </div>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="mob-no-spc" style="vertical-align:top;padding-top:0px;padding-right:75px;padding-bottom:0px;padding-left:75px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-text" style="font-size:0px;padding:0px;padding-top:0px;padding-right:10px;padding-bottom:0px;padding-left:10px;word-break:break-word;">
                                                                                  <div style="font-family:'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif;font-size:14px;font-style:Normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;color:#002961;">
                                                                                    <p> </p>
                                                                                    <p style="padding-bottom:0">
                                                                                      <span style="color: rgb(255, 105, 67);">Nous tenions à vous remercier pour votre commande <span style="font-weight: bold;">{vendor}</span></span><!-- notionvc: 193144de-8d01-41fd-bc92-9218fa32dfcb -->
                                                                                    </p>
                                                                                  </div>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="mob-no-spc" style="vertical-align:top;padding-top:0px;padding-right:75px;padding-bottom:0px;padding-left:75px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-text" style="font-size:0px;padding:0px;padding-top:0px;padding-right:10px;padding-bottom:0px;padding-left:10px;word-break:break-word;">
                                                                                  <div style="font-family:'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif;font-size:14px;font-style:Normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;color:#002961;">
                                                                                    <p> </p>
                                                                                    <p style="padding-bottom:0">
                                                                                      <span style="font-weight: bold; color: rgb(0, 41, 97); font-size: 20px;"><span style="color: #ff6943;"><span style="color: rgb(0, 41, 97);">"""
  if len(line_item_ids) == 1:
    BODY_HTML += """VOTRE CODE D'ACTIVATION"""
  else: BODY_HTML += """VOS CODES D'ACTIVATION"""
  BODY_HTML += """ :</span></span></span><!-- notionvc: 193144de-8d01-41fd-bc92-9218fa32dfcb -->
                                                                                    </p>
                                                                                  </div>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="vertical-align:top;padding-top:15px;padding-right:75px;padding-bottom:15px;padding-left:75px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-button" style="font-size:0px;padding:0px;word-break:break-word;" vertical-align="middle">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:separate;width:100%;line-height:100%;">
                                                                                    <tr>
                                                                                      <td align="center" bgcolor="#FCF5EE" role="presentation" style="border:none;border-bottom:solid 3px #002961;border-left:solid 3px #002961;border-radius:6px;border-right:solid 3px #002961;border-top:solid 3px #002961;cursor:auto;font-style:Normal;mso-padding-alt:11px 0px 11px 0px;background:#FCF5EE;" valign="middle">"""
  for id in line_item_ids:
      codes = select_codes_from_lineItem(connexion, id)
      grouped_code = defaultdict(list)
      for sku, code in codes:
        grouped_code[sku].append(code)
        for sku, codes in grouped_code.items():
            product_title = get_product_name_by_sku(event, sku)
            BODY_HTML += f"""<p href="" style='padding-bottom:0; display:inline-block; background:#FCF5EE; color:#002961; font-family:"Work Sans", Arial, "Helvetica Neue", Helvetica, sans-serif; font-size:15px; font-style:Normal; font-weight:400; line-height:100%; letter-spacing:0; margin:0; text-decoration:none; text-transform:none; padding:11px 0 11px 0; mso-padding-alt:0; border-radius:6px'>{product_title} : <span style="font-weight: bold">{code}</span></p>"""
            BODY_HTML += "<br />"
  BODY_HTML += """                                                                      </p>
                                                                                      </td>
                                                                                    </tr>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="mob-no-spc" style="vertical-align:top;padding-top:0px;padding-right:75px;padding-bottom:0px;padding-left:75px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-text" style="font-size:0px;padding:0px;padding-top:0px;padding-right:10px;padding-bottom:0px;padding-left:10px;word-break:break-word;">
                                                                                  <div style="font-family:'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif;font-size:14px;font-style:Normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;color:#002961;">"""
  for id in line_item_ids:
    codes = select_codes_from_lineItem(connexion, id)
    for sku, code in codes:
      try:
        product_id = get_product_id_by_sku(event, sku)
        metafield = retrieve_shopify_data(product_id)
        if len(metafield) > 1:
          BODY_HTML += """<p>
          <span style="font-weight: bold; color: rgb(0, 41, 97); font-size: 20px;"><span style="color: #ff6943;"><span style="color: rgb(0, 41, 97);"><br/>COMMENT ÇA MARCHE ?</span></span></span><!-- notionvc: 193144de-8d01-41fd-bc92-9218fa32dfcb -->
          </p>"""
          BODY_HTML += f"""<p style="padding-bottom:0">{metafield[1]}</p>"""
          if len(metafield) == 3:
            BODY_HTML += f"""<p style="padding-bottom:0">{metafield[2]}</p>"""
      except Exception as e:
        print("Can't find metafields from the mail template", e)
        pass
  

  BODY_HTML += """                                                               </div>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="mob-no-spc" style="vertical-align:top;padding-top:0px;padding-right:75px;padding-bottom:0px;padding-left:75px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-text" style="font-size:0px;padding:0px;padding-top:0px;padding-right:10px;padding-bottom:0px;padding-left:10px;word-break:break-word;">
                                                                                  <div style="font-family:'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif;font-size:14px;font-style:Normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;color:#002961;">
                                                                                    <p>
                                                                                      <span style="font-weight: bold; color: rgb(0, 41, 97); font-size: 20px;"><span style="color: #ff6943;"><span style="color: rgb(0, 41, 97);"><br/>CONDITIONS &amp; VALIDITÉ</span></span></span><!-- notionvc: 193144de-8d01-41fd-bc92-9218fa32dfcb -->
                                                                                    </p>"""
  for id in line_item_ids:
    codes = select_codes_from_lineItem(connexion, id)
    try:
      for sku, code in codes:       
        product_id = get_product_id_by_sku(event, sku)
        metafield = retrieve_shopify_data(product_id)
        BODY_HTML += f"""<p style="padding-bottom:0">{metafield[0]}</p>"""
    except:
      pass
      
  BODY_HTML +="""
                                                                                  </div>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="vertical-align:top;padding-top:40px;padding-right:75px;padding-bottom:40px;padding-left:75px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-button" style="font-size:0px;padding:0px;word-break:break-word;" vertical-align="middle">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:separate;width:100%;line-height:100%;">
                                                                                    <tr>
                                                                                      <td align="center" bgcolor="#002961" role="presentation" style="border:none;border-radius:5px;cursor:auto;font-style:Normal;mso-padding-alt:11px 0px 11px 0px;background:#002961;" valign="middle"> <a href="https://thebradery.com/" style='color:#FFF; font-style:Normal; font-weight:400; text-decoration:none; display:inline-block; background:#002961; font-family:"Work Sans", Arial, "Helvetica Neue", Helvetica, sans-serif; font-size:15px; line-height:100%; letter-spacing:0; margin:0; text-transform:none; padding:11px 0 11px 0; mso-padding-alt:0; border-radius:5px' target="_blank"> VOIR LES VENTES EN COURS </a> </td>
                                                                                    </tr>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                              </div>
                                                              <!--[if true]>
                                                            </td>
                                                            <![endif]--> 
                                                          </div>
                                                          <!--[if true]>
                                                        </tr>
                                                      </table>
                                                      <![endif]--> <!--[if true]>
                                                      <table border="0" cellpadding="0" cellspacing="0" width="600" style="width:600px;direction:ltr">
                                                        <tr>
                                                          <![endif]--> 
                                                          <div class="kl-row" style="display:table;table-layout:fixed;width:100%;">
                                                            <!--[if true]>
                                                            <td style="vertical-align:middle;width:600px;">
                                                              <![endif]--> 
                                                              <div class="kl-column" style="display:table-cell;vertical-align:middle;width:100%;">
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="vertical-align:top;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="left" class="kl-image" style="font-size:0px;word-break:break-word;">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                    <tbody>
                                                                                      <tr>
                                                                                        <td class="kl-img-base-auto-width" style="border:0;padding:0px 0px 0px 0px;width:600px;" valign="top"> <a href="https://app.adjust.com/18r2rwnp" style="color:#6487BA; font-style:normal; font-weight:normal; text-decoration:underline"> <img src="https://d3k81ch9hvuctc.cloudfront.net/company/KQsfB7/images/f98ebc35-a5de-475b-9fab-dcf5a2264ace.png" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" width="600"/> </a> </td>
                                                                                      </tr>
                                                                                    </tbody>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                              </div>
                                                              <!--[if true]>
                                                            </td>
                                                            <![endif]--> 
                                                          </div>
                                                          <!--[if true]>
                                                        </tr>
                                                      </table>
                                                      <![endif]--> 
                                                    </div>
                                                    <!--[if mso | IE]>
                                                  </table>
                                                  <![endif]--> 
                                                </td>
                                              </tr>
                                            </tbody>
                                          </table>
                                        </div>
                                        <!--[if mso | IE]>
                                      </td>
                                    </tr>
                                  </table>
                                </table>
                                <![endif]--> 
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <!--[if mso | IE]>
                    </td>
                  </tr>
                </table>
                <![endif]--> 
              </td>
            </tr>
          </tbody>
        </table>
        <table align="center" border="0" cellpadding="0" cellspacing="0" class="kl-section" role="presentation" style="width:100%;">
          <tbody>
            <tr>
              <td>
                <!--[if mso | IE]>
                <table align="center" border="0" cellpadding="0" cellspacing="0" class="kl-section-outlook" style="width:600px;" width="600" >
                  <tr>
                    <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                      <![endif]--> 
                      <div style="margin:0px auto;max-width:600px;">
                        <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                          <tbody>
                            <tr>
                              <td style="direction:ltr;font-size:0px;padding:0px;text-align:center;">
                                <!--[if mso | IE]>
                                <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                  <table align="center" border="0" cellpadding="0" cellspacing="0" class="" style="width:600px;" width="600" bgcolor="#FCF5EE" >
                                    <tr>
                                      <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
                                        <![endif]--> 
                                        <div style="background:#FCF5EE;background-color:#FCF5EE;margin:0px auto;border-radius:0px 0px 0px 0px;max-width:600px;">
                                          <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#FCF5EE;background-color:#FCF5EE;width:100%;border-radius:0px 0px 0px 0px;">
                                            <tbody>
                                              <tr>
                                                <td style="direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-left:0px;padding-right:0px;padding-top:0px;text-align:center;">
                                                  <!--[if mso | IE]>
                                                  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
                                                    <![endif]--> 
                                                    <div class="content-padding last">
                                                      <!--[if true]>
                                                      <table border="0" cellpadding="0" cellspacing="0" width="600" style="width:600px;direction:ltr">
                                                        <tr>
                                                          <![endif]--> 
                                                          <div class="kl-row colstack" style="display:table;table-layout:fixed;width:100%;">
                                                            <!--[if true]>
                                                            <td style="vertical-align:top;width:600px;">
                                                              <![endif]--> 
                                                              <div class="kl-column" style="display:table-cell;vertical-align:top;width:100%;">
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="vertical-align:top;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="left" class="kl-image" style="font-size:0px;word-break:break-word;">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                    <tbody>
                                                                                      <tr>
                                                                                        <td class="kl-img-base-auto-width" style="border:0;padding:0px 0px 0px 0px;width:600px;" valign="top"> <a href="https://thebradery.com/" style="color:#6487BA; font-style:normal; font-weight:normal; text-decoration:underline"> <img src="https://d3k81ch9hvuctc.cloudfront.net/company/KQsfB7/images/44189c78-06ac-402f-b7d9-4083eec27f7c.jpeg" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" width="600"/> </a> </td>
                                                                                      </tr>
                                                                                    </tbody>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="vertical-align:top;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="left" class="kl-table" style="font-size:0px;padding:0px;word-break:break-word;">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="color:#000000;font-family:Ubuntu, Helvetica, Arial, sans-serif;font-size:13px;line-height:22px;table-layout:fixed;width:100%;border:none;" width="100%">
                                                                                    <thead> </thead>
                                                                                    <tbody>
                                                                                      <tr>
                                                                                        <td class="kl-table-subblock" style="width:auto;overflow:hidden;vertical-align:top;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
                                                                                          <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                                                            <tr>
                                                                                              <td align="left" class="" style="font-size:0px;word-break:break-word;">
                                                                                                <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                                  <tbody>
                                                                                                    <tr>
                                                                                                      <td class="kl-img-base-auto-width" style="border:0;padding:0;width:600px;" valign="top"> <a href="https://www.instagram.com/thebradery/" style="color:#6487BA; font-style:normal; font-weight:normal; text-decoration:underline"> <img alt="" src="https://d3k81ch9hvuctc.cloudfront.net/company/KQsfB7/images/46512602-3893-4fec-b8f6-aca70f9c1d1a.png" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" title="" width="600"/> </a> </td>
                                                                                                    </tr>
                                                                                                  </tbody>
                                                                                                </table>
                                                                                              </td>
                                                                                            </tr>
                                                                                          </table>
                                                                                        </td>
                                                                                        <td class="kl-table-subblock" style="width:auto;overflow:hidden;vertical-align:top;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
                                                                                          <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                                                            <tr>
                                                                                              <td align="left" class="" style="font-size:0px;word-break:break-word;">
                                                                                                <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                                  <tbody>
                                                                                                    <tr>
                                                                                                      <td class="kl-img-base-auto-width" style="border:0;padding:0;width:600px;" valign="top"> <a href="https://www.tiktok.com/@thebradery" style="color:#6487BA; font-style:normal; font-weight:normal; text-decoration:underline"> <img alt="" src="https://d3k81ch9hvuctc.cloudfront.net/company/KQsfB7/images/b2d2d476-e5fe-489d-af9f-dd7075ddb719.png" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" title="" width="600"/> </a> </td>
                                                                                                    </tr>
                                                                                                  </tbody>
                                                                                                </table>
                                                                                              </td>
                                                                                            </tr>
                                                                                          </table>
                                                                                        </td>
                                                                                      </tr>
                                                                                    </tbody>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <!--[if !mso]><!-->
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper kl-text-table-layout mobile-only" style="display:none; font-size:0; text-align:left; direction:ltr; vertical-align:top; width:100%">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="background-color:#002961;vertical-align:top;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-text" style="font-size:0px;padding:0px;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;word-break:break-word;">
                                                                                  <div style="font-family:'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif;font-size:14px;font-style:Normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;color:#002961;">
                                                                                    <p class="p1"><span style="font-size: 7px; color: #6487ba; font-family: 'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif; font-weight: 400;"><em>Cet e-mail a été envoyé à {{ email|default:'' }}. </em></span></p>
                                                                                    <p class="p1"><span style="font-size: 7px; color: #6487ba; font-family: 'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif; font-weight: 400;"><em>Modifier mes {% manage_preferences 'pr&eacute;f&eacute;rences' %} ou me {% unsubscribe 'd&eacute;sinscrire' %} de la newsletter.</em> </span></p>
                                                                                    <p class="p1" style="padding-bottom:0"><span style="font-size: 7px; color: #6487ba; font-family: 'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif; font-weight: 400;"><em>Vous disposez d' un droit d' accès, de modification, d'opposition et de suppression des données vous concernant, que vous pouvez exercer sur simple demande écrite adressée au service client.</em></span></p>
                                                                                  </div>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <!--<![endif]--><!--[if !mso]><!-->
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper mobile-only" style="display:none; font-size:0; text-align:left; direction:ltr; vertical-align:top; width:100%">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="background-color:#002961;vertical-align:top;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="left" class="kl-image" style="font-size:0px;word-break:break-word;">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                    <tbody>
                                                                                      <tr>
                                                                                        <td class="kl-img-base-auto-width" style="border:0;padding:0px 0px 0px 0px;width:600px;" valign="top"><a href="https://thebradery.com/" style="color:#6487BA; font-style:normal; font-weight:normal; text-decoration:underline"><img src="https://d3k81ch9hvuctc.cloudfront.net/company/KQsfB7/images/52308c61-5a99-4d85-80e7-c6b34ee3eec2.png" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" width="600"/></a></td>
                                                                                      </tr>
                                                                                    </tbody>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <!--<![endif]--> 
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper kl-text-table-layout desktop-only" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="mob-no-spc" style="background-color:#002961;vertical-align:top;padding-top:0px;padding-right:50px;padding-bottom:0px;padding-left:50px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="center" class="kl-text" style="font-size:0px;padding:0px;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;word-break:break-word;">
                                                                                  <div style="font-family:'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif;font-size:14px;font-style:Normal;font-weight:400;letter-spacing:0px;line-height:1.3;text-align:center;color:#002961;">
                                                                                    <p class="p1"><span style="font-size: 9px; color: #6487ba; font-family: 'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif; font-weight: 400;"><em>Cet e-mail a été envoyé à {{ email|default:'' }}. </em></span></p>
                                                                                    <p class="p1"><span style="font-size: 9px; color: #6487ba; font-family: 'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif; font-weight: 400;"><em>Modifier mes {% manage_preferences 'pr&eacute;f&eacute;rences' %} ou me {% unsubscribe 'd&eacute;sinscrire' %} de la newsletter.</em> </span></p>
                                                                                    <p class="p1" style="padding-bottom:0"><span style="font-size: 9px; color: #6487ba; font-family: 'Work Sans', Arial, 'Helvetica Neue', Helvetica, sans-serif; font-weight: 400;"><em>Vous disposez d' un droit d' accès, de modification, d'opposition et de suppression des données vous concernant, que vous pouvez exercer sur simple demande écrite adressée au service client.</em></span></p>
                                                                                  </div>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                                <div class="mj-column-per-100 mj-outlook-group-fix component-wrapper desktop-only" style="font-size:0px;text-align:left;direction:ltr;vertical-align:top;width:100%;">
                                                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
                                                                    <tbody>
                                                                      <tr>
                                                                        <td class="" style="background-color:#002961;vertical-align:top;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;">
                                                                          <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="" width="100%">
                                                                            <tbody>
                                                                              <tr>
                                                                                <td align="left" class="kl-image" style="font-size:0px;word-break:break-word;">
                                                                                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border-spacing:0px;">
                                                                                    <tbody>
                                                                                      <tr>
                                                                                        <td class="kl-img-base-auto-width" style="border:0;padding:0px 0px 0px 0px;width:600px;" valign="top"> <a href="https://thebradery.com/" style="color:#6487BA; font-style:normal; font-weight:normal; text-decoration:underline"> <img src="https://d3k81ch9hvuctc.cloudfront.net/company/KQsfB7/images/4af3ce8b-4f23-45f9-89ed-ae0a8dc545bd.png" style="display:block;outline:none;text-decoration:none;height:auto;font-size:13px;width:100%;" width="600"/> </a> </td>
                                                                                      </tr>
                                                                                    </tbody>
                                                                                  </table>
                                                                                </td>
                                                                              </tr>
                                                                            </tbody>
                                                                          </table>
                                                                        </td>
                                                                      </tr>
                                                                    </tbody>
                                                                  </table>
                                                                </div>
                                                              </div>
                                                              <!--[if true]>
                                                            </td>
                                                            <![endif]--> 
                                                          </div>
                                                          <!--[if true]>
                                                        </tr>
                                                      </table>
                                                      <![endif]--> 
                                                    </div>
                                                    <!--[if mso | IE]>
                                                  </table>
                                                  <![endif]--> 
                                                </td>
                                              </tr>
                                            </tbody>
                                          </table>
                                        </div>
                                        <!--[if mso | IE]>
                                      </td>
                                    </tr>
                                  </table>
                                </table>
                                <![endif]--> 
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <!--[if mso | IE]>
                    </td>
                  </tr>
                </table>
                <![endif]--> 
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </body>
</html>"""
  
  return BODY_HTML