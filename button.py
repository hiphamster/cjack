from flask import Flask, render_template, redirect
from jinja2 import Template
import cjack

app = Flask(__name__)


@app.route('/')
def home():
    home_tpl = Template('''<html>
        <head>
            <title>CJACK BUTTON</title>
            <link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"></script>
            <script type="text/javascript" src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"></script>
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
            <style>
                .loader_s {
                  display: none;
                  border: 16px solid #f3f3f3;
                  border-radius: 50%;
                  border-top: 16px solid #4CAF4F;
                  width: 100px;
                  height:100px;
                  -webkit-animation: spin 2s linear infinite; /* Safari */
                  animation: spin 2s linear infinite;
                }

                /* Safari */
                @-webkit-keyframes spin {
                  0% { -webkit-transform: rotate(0deg); }
                  100% { -webkit-transform: rotate(360deg); }
                }

                @keyframes spin {
                  0% { transform: rotate(0deg); }
                  100% { transform: rotate(360deg); }
                }
            </style>

            <script>
                $(document).ready(function(){
                    $("#blueLink").click(function() {
                        $("#loader").show();
                        $("#blueLink").hide();
                    });
                });
            </script>
        </head
        <body>
            <div class="container-fluid">
                <div class="row">
                    <div class="col col-sm-12" style="margin: 35px; border: none 1px #ABCDEF;">

                        <a
                            id="disabledLinke"
                            class="btn btn-lg btn-block" 
                            href="/snap"
                            role="button"
                            style="font-size: 50px; max-width: 500px; margin: auto;">
                            <div id="loader" class="loader_s"></div>
                        </a>
                    </div>

                </div>


                <div class="row">
                    <div class="col col-sm-12" style="margin: 35px; border: none 1px #ABCDEF;">
                        <a
                            id="blueLink"
                            class="btn btn-primary btn-lg btn-block" 
                            href="/snap"
                            role="button"
                            style="font-size: 50px; max-width: 500px; margin: auto;">
                                SNAP!
                        </a>
                    </div>
                </div>
            </div
        </body>
    </html>''')

    return home_tpl.render()

@app.route('/snap')
def snap():
    cjack.main()
    return redirect('/') 




