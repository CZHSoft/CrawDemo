using System;
using System.Collections.Generic;
using System.Data.Entity;
using System.Linq;
using System.Text;

namespace CrawClient.Models
{
    public class DemoContext : DbContext
    {
        public DbSet<BlackList> BlackLists { get; set; }
    }
}
