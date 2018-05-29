<style lang="scss" scoped>
  .dao-table-container {
    padding-top: 0;
  }
  .dao-table-toolbar {
    height: auto;
    margin-bottom: 10px;
  }

  .table-filters .refresh-btn {
    height: 32px;
    padding: 8px 7px;
  }
  .search-btn {
    padding: 8px 7px;
    margin-left: 10px;
  }
  .down-link {
    text-decoration: none;
  }
</style>
<template>
  <div class="log-dialog-wrap">
    <dao-dialog
      :config="config"
      :visible.sync="isShow">
      <Log :logs="logs"></Log>
      <div slot="footer">
        <a :href="logUrl" class="dao-btn blue down-link">
          下载日志
        </a>
      </div>
    </dao-dialog>
  </div>
</template>
<script>
import Log from '../log/Log';

export default {
  name: 'LogDialog',
  props: {
    visible: {
      type: Boolean,
      require: true,
      default: false,
    },
    logs: String,
    logUrl: String,
  },
  data() {
    return {
      config: {
        type: 'normal',
        title: '日志',
        showHeader: true,
        showFooter: true,
        closeOnClickOutside: true,
        closeOnPressEscape: true,
      },
      isShow: this.visible,
    };
  },
  computed: {
  },
  methods: {
    cancel() {
      this.close();
    },
    close() {
      this.$emit('update:visible', false);
      // this.isShow = false;
    },
  },

  watch: {
    visible(newV) {
      if (newV !== this.isShow) {
        this.isShow = newV;
      }
    },
    isShow(newV) {
      if (newV === this.visible) return;
      this.$emit('update:visible', newV);
    },
  },
  components: {
    Log,
  },
};
</script>
