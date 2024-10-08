document.querySelectorAll(".productsSection .products .product").forEach(function (self) {
    var timeline = new TimelineMax();
    var tween1 = TweenMax.from(self, 1, {opacity: 0, ease: Linear.easeNone});
    var tween2 = TweenMax.to(self, 1, {opacity: 1, ease: Linear.easeNone});
    timeline
        .add(tween1)
        .add(tween2);

    new ScrollMagic.Scene({triggerElement: self, triggerHook: 1, duration: "100%", reverse: true})
        // .setTween(self, 1, {opacity: 1, ease: Linear.easeNone})
        .setTween(timeline)
        .addTo(controller);
});