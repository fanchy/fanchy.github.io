<!-- Site footer
    
    <div id="footer" class="container" style="margin-top:50px">
        <nav class="navbar navbar-default navbar-fixed-bottom">
            <div class="navbar-inner navbar-content-center">
                <p class="text-muted credit" style="padding: 0px;">
                    <p class="text-center"><a href="http://www.miibeian.gov.cn/" target="_blank">沪ICP备17021230号-1</a></p>
                    
                </p>
            </div>
        </nav>
    </div>
  -->
    <div id="container">
        <div id="footer">
            <p class="text-muted credit text-center">
                <a  target="_blank">沪ICP备17021230号-1</a>
            </p>
        </div>
    </div>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->

    <script src="http://cdn.bootcss.com/jquery/1.11.2/jquery.min.js"></script>
    <script src="http://cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    <script src="http://cdn.bootcss.com/markdown.js/0.4.0/markdown.min.js"></script>
    <script src="http://cdn.bootcss.com/highlight.js/8.4/highlight.min.js"></script>
    <script>

      function Editor(input, preview) {
        this.update = function () {
            var strdata = input.value;
            if (strdata == "")
                strdata = " ";
            var a = strdata.substr(strdata.length-1, 1);
            while (a == '\n' || a == ' ' || a == '\r'){
                strdata = strdata.substr(0, strdata.length-1);
                if (strdata.length == 0)
                    break;
                a = strdata.substr(strdata.length-1, 1);
            }
            //alert(strdata+"a");
            var index = -1; //定义变量index控制索引值
            //当查找不到a，即indexOf()的值为-1时，结束循环
            var linenum = 0;
            do {
                index = strdata.indexOf("\n\n", index + 1); //使用第二个参数index+1，控制每一次查找都是从上一次查找到字符a的下一个索引位置开始
                if (index != -1) { //可以找到字符i
                    linenum += 1;
                }
            } while (index != -1);
            console.log('linenum:'+linenum);
            var genhtml = markdown.toHTML(strdata);
            
            genhtml = genhtml.replace(/<code>cpp/g, '<pre><code class="cpp">');
            genhtml = genhtml.replace(/<code>python/g, '<pre><code class="python">');
            genhtml = genhtml.replace(/<code>lua/g, '<pre><code class="lua">');
            genhtml = genhtml.replace(/<code>php/g, '<pre><code class="php">');
            genhtml = genhtml.replace(/<code>javascript/g, '<pre><code class="javascript">');
            genhtml = genhtml.replace(/code>/g, 'code></pre>');
            //
            if (linenum < 10){
                var needpx = (10 - linenum) * 80;
                genhtml += '<p style="margin-top:'+needpx+'px;"> </p>';
            }
            //alert(genhtml);
            
            preview.innerHTML = genhtml;
        };
        input.editor = this;
        this.update();
        
        //!highlight.min.js
        hljs.initHighlightingOnLoad();
        
      }
      var GetEByEd = function (id) { return document.getElementById(id); };

      new Editor(GetEByEd("text-input"), GetEByEd("markdown-preview"));
      
      //$(document).ready(function() {
      //    $('pre code').each(function(i, block) {
      //      hljs.highlightBlock(block);
      //    });
      //  });
    </script>
</body></html>
