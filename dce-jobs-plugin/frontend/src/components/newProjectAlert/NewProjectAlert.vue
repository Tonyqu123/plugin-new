<style lang="scss">
  .new-project-dialog {
    .dao-dialog-wrapper .dao-dialog-container {
      height: auto;
    }
    .manage-wrap {
      display: flex;
    }
    .manage-btn {
      margin-left: 10px;
    }

    .dao-setting-content .dao-select {
      width: 100%;
    }
  }
</style>
<template>
  <div class="new-project-dialog">
    <dao-dialog
      :config="config"
      :visible.sync="isShow"
    >
      <dao-setting-section>
        您还有执行中的任务，如果现在开始新任务，当前的进度将被清空。
      </dao-setting-section>
      <div slot="footer">
        <button class="dao-btn ghost" @click="cancel()">取消</button>
        <button class="dao-btn blue" @click="clear()">清空</button>
      </div>
    </dao-dialog>
  </div>
</template>
<script>
export default {
  name: 'NewProjectAlert',
  props: {
    visible: {
      type: Boolean,
      require: true,
      default: false,
    },
    closeProjectAlert: Function,
  },
  data() {
    return {
      config: {
        type: 'normal',
        title: '要在任务执行完毕之前，开始新任务吗？',
        showHeader: true,
        showFooter: true,
        closeOnClickOutside: true,
        closeOnPressEscape: true,
      },
      isShow: this.visible,
    };
  },
  methods: {
    cancel() {
      this.closeProjectAlert(false);
      this.close();
    },
    clear() {
      this.closeProjectAlert(true);
      this.close();
    },
    close() {
      this.isShow = false;
    },
  },
  mounted() {
  },
  watch: {
    visible(newV, oldV) {
      if (newV === oldV || newV === this.isShow) return;
      this.isShow = newV;
    },
    isShow(newV) {
      if (newV === this.visible) return;
      this.$emit('update:visible', newV);
    },
  },
};
</script>
