using StackExchange.Redis;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace CrawClient.Common
{
    public class RedisHelper
    {
        // redis config
        private static ConfigurationOptions configurationOptions = ConfigurationOptions.Parse("127.0.0.1:6379,password=1,connectTimeout=2000");

        //the lock for singleton
        private static readonly object Locker = new object();

        //singleton
        private static ConnectionMultiplexer redisConn;

        //singleton
        public static ConnectionMultiplexer getRedisConn()
        {

            if (redisConn == null)
            {
                lock (Locker)
                {
                    if (redisConn == null || !redisConn.IsConnected)
                    {
                        redisConn = ConnectionMultiplexer.Connect(configurationOptions);
                    }
                }
            }
            return redisConn;
        }
    }
}
