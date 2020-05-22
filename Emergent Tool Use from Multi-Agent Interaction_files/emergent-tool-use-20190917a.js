// YouTube hero video
var tag = document.createElement('script');
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('hero-video', {
    height: '100%',
    width: '100%',
    videoId: 'kopoLzvh5jY',
    playerVars: {
      color: 'white',
      rel: 0,
    },
    events: {
      'onReady': onPlayerReady,
    }
  });
}

function onPlayerReady(event) {
  var trigger = document.querySelector('.js-video-trigger');
  if (!trigger) return;
  trigger.addEventListener('click', function (e) {
    e.preventDefault();
    event.target.playVideo();
  });
}

// lazy load videos
var initCustomLazyLoad = function () { // from blazy.js included in openai.com
  /* global Blazy:true */
  var lazy = new Blazy({ // eslint-disable-line no-unused-vars
    selector: '.js-custom-lazy',
    successClass: 'js-custom-lazy-loaded',
    errorClass: 'js-custom-lazy-error',
    loadInvisible: true,
    offset: 1200,
    success: initVimeo,
  });
};


// set up player objects on each of the videos
// https://github.com/vimeo/player.js/
var playerObjects = {};
var initVimeo = function (videoEl) {
  var id = videoEl.getAttribute('data-id');
  var player = new Vimeo.Player(videoEl);
  player.on('play', function () {
    videoEl.classList.add('is-playing');
  });
  player.on('pause', function () {
    videoEl.classList.remove('is-playing');
  });
  playerObjects[id] = player; // keep track of players by id
};


// monitor scroll, and play video only if in viewport
var initScrollMonitor = function () {
  var items = document.querySelectorAll('[data-video]');
  if (!items) return;

  var watchers = [];
  for (i = 0, l = items.length; i < l; i++) {
    var item = items[i];
    var watcher = scrollMonitor.create(item, 120);
    watchers[i] = watcher;
    watcher.stateChange(listener);
  }
  for (i = 0, l = watchers.length; i < l; i++) {
    listener(null, watchers[i]);
  }

  function listener(event, watcher) {
    if (watcher.isInViewport) {
      enableVideo(watcher.watchItem.getAttribute('data-id'));
    } else {
      disableVideo(watcher.watchItem.getAttribute('data-id'));
    }
  }
};

var enableVideo = function (id) {
  if (!playerObjects[id]) return;
  playerObjects[id].play();
};
var disableVideo = function (id) {
  if (!playerObjects[id]) return;
  playerObjects[id].pause();
  playerObjects[id].setCurrentTime(0); // restart
};

// monitor scroll for emergence videos to activate links
var initEmergenceScrollMonitor = function () {
  var items = document.querySelectorAll('#emergence [data-monitor]');
  if (!items) return;

  var watchers = [];
  for (i = 0, l = items.length; i < l; i++) {
    var item = items[i];
    var watcher = scrollMonitor.create(item, 0);
    watchers[i] = watcher;
    watcher.stateChange(listener);
  }
  for (i = 0, l = watchers.length; i < l; i++) {
    listener(null, watchers[i]);
  }

  function listener(event, watcher) {
    if (watcher.isFullyInViewport) {
      setActiveLink(watcher.watchItem.getAttribute('id'), watcher.watchItem.parentElement.parentElement.getAttribute('id'));
      setActiveOverlay(watcher.watchItem.getAttribute('id'), watcher.watchItem.parentElement.parentElement.getAttribute('id'));
      // updateUrl(watcher.watchItem.getAttribute('id'));
    }
  }
};

var setActiveLink = function (id, parentId) {
  var activeLink = document.querySelector(".tick-link[href='#" + id + "']");
  if (!activeLink) return;
  removeActiveLinks(parentId);
  activeLink.classList.add('is-active');

};
var setActiveOverlay = function (id, parentId) {
  var activeOverlay = document.querySelector(".rect-overlay[data-overlay='" + id + "']");
  if (!activeOverlay) return;
  removeActiveOverlays(parentId);
  activeOverlay.classList.add('is-active');
};
var removeActiveLinks = function (parentId) {
  var links = document.querySelectorAll('#' + parentId + ' .tick-link');
  if (!links.length) return;
  links.forEach(l => l.classList.remove('is-active'));
};
var removeActiveOverlays = function (parentId) {
  var overlays = document.querySelectorAll('#' + parentId + ' .rect-overlay');
  if (!overlays.length) return;
  overlays.forEach(o => o.classList.remove('is-active'));
};

// var updateUrl = function (url) {
//   if (url) {
//     window.history.replaceState(null, null, window.location.pathname + '#' + url);
//   } else { // homepage
//     window.history.replaceState(null, null, window.location.pathname);
//   }
// }

// smooth scroll for emergence links
var initSmoothScroll = function () { // gets called upon value return from Observable notebook
  var links = document.querySelectorAll('.tick-link');
  // if (links.length != 12) return;

  links.forEach(l => {
    l.addEventListener('click', (e) => {
      e.preventDefault();
      var href = l.getAttribute('href');
      document.querySelector(href).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
};

// call everything
document.addEventListener('DOMContentLoaded', function () {
  initCustomLazyLoad();
  initScrollMonitor();
  initEmergenceScrollMonitor();
});
