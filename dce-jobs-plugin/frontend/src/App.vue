<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>
<script>
export default {
  name: 'app',
};
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #f1f3f6;
  .dao-dialog-backdrop {
    background-color: transparent;

    &.backdrop__scroll {
      background-color: transparent;
    }
  }
}
.noty_theme__mint.noty_bar .noty_body,
.noty_theme__relax.noty_bar .noty_body {
  text-align: center;
}

%dialog .dao-dialog-backdrop .dao-dialog-wrapper.dao-dialog__normal {
  padding: 0;
  vertical-align: top;
}

.new-project-dialog,
.edit-job-dialog,
.log-dialog-wrap {
  @extend %dialog;
}

.new-project-dialog .dao-dialog-container {
  margin-top: 40px;
}
.edit-job-dialog {
  .deleteDialog .dao-dialog-container {
    margin-top: 60px;
  }
  .dao-dialog-container {
    margin-top: 20px;
  }
}

.log-dialog-wrap .dao-dialog-container {
  width: 800px;
}

.history-dialog .dao-dialog-wrapper[size='resize'] .dao-dialog-container {
  width: 95%;
  height: auto;
  top: 30%;
  resize: horizontal;
}

.container-list {
  .dao-table-main {
    overflow: inherit;
  }

  .dao-table.slat {
    td:not(.tootip-td),
    th {
      overflow: hidden;
      text-overflow : ellipsis;
    }

    td,
    th {
      min-width: 75px;
    }
  }

  .tootip-td {
    .dao-tooltip {
      width: calc(100% - 10px);
    }
    .dao-tooltip-rel {
      text-overflow : ellipsis;
      overflow: hidden;
    }

    .dao-tooltip-inner {
      white-space: initial;
    }
  }
}
</style>
