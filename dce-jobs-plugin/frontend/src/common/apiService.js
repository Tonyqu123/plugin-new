import Vue from 'vue';
import Api from './apiConfig';


export default {
/**
 *
 * DCE 接口
 *
 */
 // get services
  getServices(name) {
    const { dceBaseUrl, apps } = Api;
    return Vue.http
      .get(`${dceBaseUrl}/${apps}/${name}`)
      .then(res => res.body, (error) => {
        console.log(error);
        throw Error(error);
      });
  },
  // get tasks (容器列表)
  /* eslint-disable */
  getTasks(id) {
    const { dceBaseUrl, tasks } = Api;
    const params = {
      service: [id],
    };
    return Vue.http
      .get(`${dceBaseUrl}/${tasks}`, {
        params: {
          filters: JSON.stringify(params),
        },
      })
      .then(res => res.body
        .filter((item) => item.DesiredState === 'running' && item.Status.State === 'running')
          .sort((a, b) => a.Slot - b.Slot),
        (error) => {
        throw Error(error);
      });
  },
/**
 *
 * 作业相关
 *
 */
  // get 作业
  getJobs(appName) {
    const { baseUrl, jobs } = Api;
    return Vue.http
      .get(`${baseUrl}/${jobs}`, {
        params: {
          AppName: appName,
        },
      })
      .then(res => res.body);
  },
  // 创建 作业
  createJobs(data) {
    const { baseUrl, jobs } = Api;
    return Vue.http
      .post(`${baseUrl}/${jobs}`, data)
      .then(res => res.data);
  },
  // 启动执行作业
  startJobs(id, data) {
    const { baseUrl, jobs } = Api;
    return Vue.http
      .post(`${baseUrl}/${jobs}/${id}/start`, data)
      .then(res => res.data);
  },
  // 修改作业
  putJobs(id, data) {
    const { baseUrl, jobs } = Api;
    return Vue.http
      .put(`${baseUrl}/${jobs}/${id}`, data)
      .then(res => res.data);
  },
  // 删除作业
  deleteJobs(id) {
    const { baseUrl, jobs } = Api;
    return Vue.http
      .delete(`${baseUrl}/${jobs}/${id}`)
      .then(res => res.data);
  },
  // 查看作业上一次的结果
  inspectJobs(id, timestamp) {
    const { baseUrl, jobs } = Api;
    return Vue.http
      .get(`${baseUrl}/${jobs}/${id}/inspect/${timestamp}`)
      .then(res => res.data.Result);
  },
  // 查看当前应用的所有执行作业的历史
  getJobHistory(appName) {
    const params = {
      AppName: appName,
    };
    const { baseUrl, jobs } = Api;
    return Vue.http
      .get(`${baseUrl}/${jobs}/history`, { params })
      .then(res => {
        /* eslint-disable */
        return res.body.reduce((pre, cur) => {
          const tempResult = cur.Result
            .map((item) => ({
              ...item,
              JobId: cur.JobId,
            }));

          return [
            ...pre,
            ...tempResult,
          ];
        }, []);
      });
  },
};
