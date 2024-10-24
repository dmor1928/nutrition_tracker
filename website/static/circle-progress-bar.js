window.addEventListener("DOMContentLoaded", () => {
  // update circle when range change
  const pie = document.querySelectorAll(".pie");
  const range = document.querySelector('[type="range"]');

  // start the animation when the element is in the page view
  const elements = [].slice.call(document.querySelectorAll(".pie"));
  const circle = new CircularProgressBar("pie");

  // circle.initial();

  if ("IntersectionObserver" in window) {
    const config = {
      root: null,
      rootMargin: "0px",
      threshold: 0.75
    };

    const ovserver = new IntersectionObserver((entries, observer) => {
      entries.map((entry) => {
        if (entry.isIntersecting && entry.intersectionRatio > 0.75) {
          circle.initial(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, config);

    elements.map((item) => {
      ovserver.observe(item);
    });
  } else {
    elements.map((element) => {
      circle.initial(element);
    });
  }

  // global configuration
  const globalConfig = {
    speed: 30,
    animationSmooth: "1s ease-out",
    strokeBottom: 5,
    colorSlice: "#FF6D00",
    colorCircle: "#f1f1f1",
    round: true
  };

  const global = new CircularProgressBar("global", globalConfig);
  global.initial();

  // update global example when change range
  const pieGlobal = document.querySelectorAll(".global");
  range.addEventListener("input", (e) => {
    pieGlobal.forEach((el, index) => {
      const options = {
        index: index + 1,
        percent: e.target.value
      };
      global.animationTo(options);
    });
  });

  document.querySelectorAll("pre code").forEach((el) => {
    hljs.highlightElement(el);
  });
});