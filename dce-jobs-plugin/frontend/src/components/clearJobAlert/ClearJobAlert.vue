<style lang="scss">
  .new-project-dialog {
    .dao-dialog-backdrop .dao-dialog-wrapper .dao-dialog-container {
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
      <!-- @dao-dialog-open="handleOpen" -->
      <!-- @dao-dialog-cancel="handleCancel" -->
      <!-- @dao-dialog-confirm="handleConfirm" -->
      <dao-setting-section>
        您有执行中的任务，如果现在清空，当前的任务进度将被丢失。
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
  name: 'ClearJobAlert',
  props: {
    visible: {
      type: Boolean,
      require: true,
      default: false,
    },
  },
  data() {
    return {
      config: {
        type: 'normal',
        title: '您有执行中的任务，如果现在清空，当前的任务进度将被丢失。',
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
      this.close();
    },
    clear() {
      this.$emit('clearJobs');
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
