<style lang="scss" scoped>
  .log-darken {
    color: #fff;
    background-color: #151718;
    height: 450px;
    overflow: auto;
    padding: 10px 15px;

    .log-line {
      font-size: 12px;
      font-family: Consolas, "SF Mono", Courier, monospace;
      display: block;
      word-break: break-all;
      line-height: 12 * 1.4px;
      margin-bottom: 0;
      -webkit-font-smoothing: auto;

      .timestamp, .name {
        white-space: nowrap;
        color: #aab2bd;
      }
      .message {
        white-space: pre-wrap;
      }
    }
  }

</style>
<template>
  <div class="log-darken">
    <span class="message"><pre>{{ logs }}</pre></span>
    <!--
    <div class="log-line" :key="index" v-for="(log, index) in logList">
      <span class="timestamp">{{log.timestamp}}</span>
      <span class="name" v-if="!forBuild">{{log.name}}</span>
      <span class="message">{{log.message}}</span>
    </div>
    <!--
    <div class="loading" v-if="!noLogs && !logList.length">loading...</div>
    -->
    <div class="loading" v-if="!logs">当前没有日志</div>
  </div>
</template>
<script>
/* eslint-disable no-param-reassign */
  export default {
    name: 'Log',
    props: {
      logs: String,
      forApp: Boolean,
      forBuild: Boolean,
      status: String, // expect: waiting, loading, loaded
    },
    data() {
      return {
        logList: null,
        logsTimer: null,
        noLogs: true,
      };
    },
    methods: {
      logFormatForApp(allLogList) {
        const logLines = [];
        allLogList.forEach((line) => {
          if (!line) return;
          // 将 json 转化为对象
          const data = JSON.parse(this.clearCtrlChars(line));
          logLines.push({
            name: data.Name[0] === '/' ? data.Name.substring(1) : data.Name,
            timestamp: this.moment(data.Timestamp).format('YYYY-MM-DD HH:mm:ss'),
            timeId: this.moment(data.Timestamp).valueOf(),
            message: data.Message,
          });
        });
        return logLines;
      },
      /**
       * @param {string[]} logs
       */
      logFormat(logs) {
        if (!logs || !logs.length) return [];
        return logs.map(log => this.clearCtrlChars(log))
          .map(log => log.replace(/[\r]/g, '\n').split('\n'))
          .reduce((total, nxt) => total.concat(nxt))

          .map((v) => {
            try {
              // JSON 格式的构建日志
              const log = JSON.parse(v);
              // const log = angular.fromJson(v);
              const line = {
                timestamp: this.moment(log.Timestamp).format('YYYY-MM-DD HH:mm:ss'),
                message: log.Message,
              };
              return line;
            } catch (e) {
              // 非 JSON 格式的终端输出
              let line;
              if (v.match(/(.{8})\d{4}-\d\d-\d\d[A-Z]\d\d:\d\d:\d\d\.\d+Z.*/g) !== null) {
                v = v.substring(8);
                v.replace(/\d{4}-\d\d-\d\d[A-Z]\d\d:\d\d:\d\d\.\d+Z/, (time) => {
                  // 不可以使用 timeId 的排序
                  // 因为两行日志的是时间戳太接近，排序反而会打乱原有的顺序
                  line = {
                    timestamp: this.moment(time).format('YYYY-MM-DD HH:mm:ss'),
                    message: v.substring(time.length),
                  };
                });
              }

              return line;
            }
          })
          .filter(item => item);
      },
      scrollToBottom() {
        console.log('scrollToBottom');
        // this.$scope.$watch(() => this.logList.length, () => {
        //   this.$timeout(() => {
        //     this.$element.animate({
        //       scrollTop: this.$element[0].scrollHeight,
        //     }, 200);
        //   });
        // });
      },
      startLoadingTimer() {
        this.logsTimer = setTimeout(() => {
          this.noLogs = true;
        }, this.LOGS_TIMEOUT);

        // this.$scope.$on('$destroy', () => {
        //   this.clearTimer();
        // });
      },

      clearTimer() {
        clearTimeout(this.logsTimer);
      },

      /**
       * http://www.inwap.com/pdp10/ansicode.txt
       * stdout 中常见的控制字符有
       * [1A
       * [2K
       * [1B
       * 替换建议: 替换成空字符串
       */
      clearCtrlChars(str) {
        return str.replace(/\[1A|\[2K|\[1B/g, '');
      },
    },

    watch: {
      status(newV) {
        if (newV === 'loading') {
          this.startLoadingTimer();
        } else {
          this.clearTimer();
        }
      },
    },
  };
</script>
