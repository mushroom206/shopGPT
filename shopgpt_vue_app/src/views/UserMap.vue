<template>
    <div class="full-screen">
      <el-image
        class="image-container"
        :src="require('@/assets/images/LA_Demographics.png')"
        fit="contain"
      ></el-image>
      <div class="overlay" @click="handleOverlayClick">
        <div
          v-for="(circle, index) in circles"
          :key="index"
          class="circles"
          @click="handleCircleClick(index)"
          :style="{ top: circle.top, left: circle.left }"
        >
          <div class="circle1"></div>
          <div class="circle2"></div>
          <div class="circle3"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        circles: [
          { top: '33%', left: '12%' },
          { top: '55%', left: '31%' },
          { top: '30%', left: '32%' },
          { top: '32%', left: '63%' },
          // Add more circles and positions as needed
        ],
      };
    },
    methods: {
      handleCircleClick(index) {
        const currentTop = this.circles[index].top;
        const currentLeft = this.circles[index].left;
  
        const newPosition = prompt(
          `Enter new position (format: vertical horizontal)\nCurrent position: ${currentTop} ${currentLeft}`
        );
  
        if (newPosition) {
          const [newTop, newLeft] = newPosition.split(' ');
  
          // Convert inputs to numbers
          const topValue = parseInt(newTop);
          const leftValue = parseInt(newLeft);
  
          if (!isNaN(topValue) && !isNaN(leftValue)) {
            this.circles[index].top = `${topValue}%`;
            this.circles[index].left = `${leftValue}%`;
          }
        }
      },
      handleOverlayClick(event) {
        const clickedTop = `${event.clientY}px`;
        const clickedLeft = `${event.clientX}px`;
  
        // Check if the clicked position overlaps with any existing circle
        const isOverlapping = this.circles.some(
          (circle) =>
            Math.abs(parseFloat(circle.top) - event.clientY) < 10 &&
            Math.abs(parseFloat(circle.left) - event.clientX) < 10
        );
  
        if (!isOverlapping) {
          this.circles.push({ top: clickedTop, left: clickedLeft });
        }
      },
    },
  };
  </script>

  <style>
.full-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: black; /* Optional background color */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999; /* Adjust as needed */
}

.image-container {
  max-width: 100%;
  max-height: 100%;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0);
  z-index: 1; /* Place the overlay above the image */
}

.circles {
  height: 10vmin;
  position: absolute;
  width: 10vmin;
  
  > div {
    animation: growAndFade 3s infinite ease-out;
    background-color: rgb(25, 2, 35);
    border-radius: 50%;
    height: 100%;
    opacity: 0;
    position: absolute;
    width: 100%;
  }
  
  .circle1 {
    animation-delay: 1s;    
  }
  .circle2 {
    animation-delay: 2s; 
  }
  .circle3 {
    animation-delay: 3s;
  }
}

@keyframes growAndFade {
  0% {
    opacity: .25;
    transform: scale(0);
  }
  100% {
    opacity: 0;
    transform: scale(1);
  }
}

body {
  align-items: center;
  display: flex;
  height: 100vh;
  justify-content: center;
  margin: 0;
}
</style>