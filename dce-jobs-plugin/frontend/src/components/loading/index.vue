<style lang="scss" scoped>
  ::-webkit-scrollbar {
    width: 13px;
    height: 8px;
  }

  ::-webkit-scrollbar-track {
    background: transparent;
  }

  ::-webkit-scrollbar-thumb {
    border-radius: 8px;
    width: 5px;
    height: 5px;
    background-color: #bbb;
    background-clip: padding-box;
    border-right: 3px solid transparent;
    border-left: 4px solid transparent;
    border-top: 3px solid transparent;
  }

  ::-webkit-scrollbar-thumb:hover {
    background-color: #888;
  }

  @keyframes scale-sport{
    0% {
      -webkit-transform: scaley(1);
      transform: scaley(1);
    }
    50% {
      -webkit-transform: scaley(0.4);
      transform: scaley(0.4);
    }
    100% {
      -webkit-transform: scaley(1);
      transform: scaley(1);
    }
  }
  .loading{
    box-sizing: border-box;
    display: flex;
    flex: 0 1 auto;
    flex-direction: column;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 25%;
    max-width: 25%;
    height: 200px;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
  }
  .line-scale > div {
    background-color: rgba(0, 0, 0, 0.4);
    width: 4px;
    height: 35px;
    border-radius: 2px;
    margin: 2px;
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
    display: inline-block;
  }
  .line-scale > div:nth-child(1) {
    -webkit-animation: scale-sport 1s 0.1s infinite cubic-bezier(.2, .68, .18, 1.08);
    animation: scale-sport 1s 0.1s infinite cubic-bezier(.2, .68, .18, 1.08);
  }
  .line-scale > div:nth-child(2) {
    -webkit-animation: scale-sport 1s 0.2s infinite cubic-bezier(.2, .68, .18, 1.08);
    animation: scale-sport 1s 0.2s infinite cubic-bezier(.2, .68, .18, 1.08);
  }
  .line-scale > div:nth-child(3) {
    -webkit-animation: scale-sport 1s 0.3s infinite cubic-bezier(.2, .68, .18, 1.08);
    animation: scale-sport 1s 0.3s infinite cubic-bezier(.2, .68, .18, 1.08);
  }
  .line-scale > div:nth-child(4) {
    -webkit-animation: scale-sport 1s 0.4s infinite cubic-bezier(.2, .68, .18, 1.08);
    animation: scale-sport 1s 0.4s infinite cubic-bezier(.2, .68, .18, 1.08);
  }
  .line-scale > div:nth-child(5) {
    -webkit-animation: scale-sport 1s 0.5s infinite cubic-bezier(.2, .68, .18, 1.08);
    animation: scale-sport 1s 0.5s infinite cubic-bezier(.2, .68, .18, 1.08);
  }
</style>
<template>
  <div class="list">
    <div class='loading'>
      <div class='line-scale'>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
  </div>
</template>
<script>
	/* eslint-disable */
  export default {
    data() {
      return {
      };
    },
    methods: {
    },
  };
</script>
