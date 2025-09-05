(function(){
  function computeCounterpartUrl(href){
    try{
      var url = new URL(href, window.location.origin);
      var parts = url.pathname.split('/').filter(Boolean);
      if(parts.length < 2) return href;
      var versionSegIndex = parts.length - 2;
      var fileIndex = parts.length - 1;
      var ver = parts[versionSegIndex];
      var file = parts[fileIndex];
      var isEn = /_en$/.test(ver) || /index_en\.html$/.test(file);
      var targetVer = isEn ? ver.replace(/_en$/, '') : (/_en$/.test(ver) ? ver : ver + '_en');
      var targetFile = file;
      if(/index_en\.html$/.test(file)) targetFile = 'index.html';
      else if(/index\.html$/.test(file)) targetFile = 'index_en.html';
      else if(/README_zh\.html$/.test(file)) targetFile = 'README.html';
      else if(/README\.html$/.test(file)) targetFile = 'README_zh.html';
      parts[versionSegIndex] = targetVer;
      parts[fileIndex] = targetFile;
      return '/' + parts.join('/') + url.search + url.hash;
    }catch(e){ return href; }
  }

  function detectIsEnglish(){
    var p = window.location.pathname;
    return /(^|\/)\w+_en\//.test(p) || /index_en\.html$/.test(p);
  }

  function placeAtSidebarBottom(host){
    var container = document.querySelector('.wy-side-scroll') || document.querySelector('.bd-sidebar__content') || document.querySelector('#rtd-sidebar') || host.parentElement;
    if(container && host && host.parentElement !== container){
      container.appendChild(host);
    }
  }

  function mount(){
    var host = document.getElementById('lang-switcher');
    if(!host) return;
    placeAtSidebarBottom(host);
    var isEn = detectIsEnglish();
    var counterpart = computeCounterpartUrl(window.location.href);
    var currentLabel = isEn ? 'English' : '中文';
    var otherLabel = isEn ? '中文' : 'English';
    host.classList.add('lang-switcher');
    host.innerHTML = '<span class="lang-current">' + currentLabel + '</span>' + ' | ' + '<a class="lang-link" href="' + counterpart + '">' + otherLabel + '</a>';
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
