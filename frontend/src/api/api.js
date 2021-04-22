import axiosInstance from './index'

const axios = axiosInstance

// 这里用来实现调取后端各种api的方法

export const showCourses = () => {
  return axios.get(`http://localhost:8000/api/courses/`)
}
