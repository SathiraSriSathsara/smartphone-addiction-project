"use strict";

document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
  const callToAction = document.querySelector(".hero__cta");
  if (!callToAction) {
    return;
  }

  callToAction.setAttribute(
    "href",
    window.SmartHabitConfig?.predictionPage ?? "predict.html",
  );
});
