import axios from 'axios'

async function authorization () {
  const storage = localStorage
  let hasLogin = false
  let username = storage.getItem('username.mysite')

  const expiredTime = Number(storage.getItem('expiredTime.mysite'))
  const current = (new Date()).getTime()
  const refreshToken = storage.getItem('refresh.mysite')

  // 初始 token 未过期
  if (expiredTime > current) {
    hasLogin = true
    console.log('authorization access')
  } else if (refreshToken !== null) {
    // 初始 token 过期
    // 申请刷新 token
    try {
      let response = await axios.post('http://localhost:8000/api/token/refresh/', {refresh: refreshToken})
      const nextExpiredTime = (new Date()).getTime() + 300000
      storage.setItem('access.mysite', response.data.access)
      storage.setItem('expiredTime.mysite', nextExpiredTime)
      storage.removeItem('refresh.mysite')
      hasLogin = true
      console.log('authorization refresh')
    } catch (error) {
      storage.clear()
      hasLogin = false
      console.log('authorization error')
    }
  } else {
    // 无任何有效 token
    storage.clear()
    hasLogin = false
    console.log('authorization exp')
  }
  console.log('authorization done')
  return [hasLogin, username]
}

export default authorization
