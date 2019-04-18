using CrawClient.Common;
using CrawClient.Models;
using Newtonsoft.Json;
using StackExchange.Redis;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;


namespace CrawClient
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        private DemoContext context;
        private IDatabase db;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            WaitingBox.Show(this, () =>
            {
                init();
            }, "正在玩命的加载，请稍后...");
        }

        private void init()
        {
            context = new DemoContext();

            var redisConn = RedisHelper.getRedisConn();
            db = redisConn.GetDatabase();

            List<JobModel> jobs = new List<JobModel>();

            string[] keys = new string[] { "51job", "zhilian", "liepin", "0757rc" };

            foreach (var key in keys)
            {
                var data = db.HashGetAll(key);

                foreach (var d in data)
                {

                    try
                    {
                        string s = d.Value.ToString().Replace("\"", "").Replace("\'", "\"");

                        dynamic json = JsonConvert.DeserializeObject<dynamic>(s);

                        jobs.Add(new JobModel()
                        {
                            Type = key,
                            Company = json.company,
                            Name = json.name,
                            Url = json.url
                        });
                    }
                    catch
                    {

                    }

                }
            }

            dataGrid.Dispatcher.Invoke(new Action(() => { dataGrid.ItemsSource = jobs; }));

        }
    }
}
