import ApiService from './apiService';

export default {
  // get services
  getServices(name) {
    return ApiService.getServices(name)
      .then(data => data.Services
        .map(({ ID, Spec }) => ({
          id: ID,
          name: Spec.Name,
        })));
  },

  // get tasks (容器列表)
  getContainers(serviceId) {
    return ApiService.getTasks(serviceId)
      .then(data => data);
  },

  /**
   * 获取 name 应用, 对应的 services 和 containers (containers 里 增加 serviceName) 组合
   * @param  {[STring]} name [应用名]
   * @return {[Object]}
   *   serviceContainers = {
   *      [serviceName]: [containers]
   *   }
   *
   */
  getServiceContainers(appName) {
    return this.getServices(appName)
      .then((services) => {
        const promiseQ = [];
        services.forEach(({ id, name }) => {
          const tempProm = this.getContainers(id)
            .then(data => ({ name, data }));
          promiseQ.push(tempProm);
        });

        return Promise.all(promiseQ)
          .then((response) => {
            const serviceContainers = {};
            response.forEach((tasks) => {
              serviceContainers[tasks.name] = tasks.data;
            });
            return serviceContainers;
          }, (error) => {
            console.error(error);
            return {};
          });
      });
  },
};
