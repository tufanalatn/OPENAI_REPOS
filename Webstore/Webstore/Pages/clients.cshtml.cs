using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using System.Data.SqlClient;

namespace Webstore.Pages
{
    public class clientsModel : PageModel
    {
        public List<clientInfo> listClients = new List<clientInfo>();
        public void OnGet()
        {
            try
            {
                string connectionString = "Data Source=TRISLAP296;Initial Catalog=WebStore;Integrated Security=True;Encrypt=False";
                using (SqlConnection connection = new SqlConnection(connectionString))
                {
                    connection.Open();
                    string sql = "SELECT * from Clients";
                    using (SqlCommand command = new SqlCommand(sql, connection))
                    {
                        using (SqlDataReader reader = command.ExecuteReader())
                        {
                            while (reader.Read())
                            {
                                clientInfo client = new clientInfo();
                                client.id = reader.GetInt32(0);
                                client.name = reader.GetString(1);
                                client.email = reader.GetString(2);
                                client.phone = reader.GetString(3);
                                client.address = reader.GetString(4);

                                listClients.Add(client);

                            }
                        }
                    }
                }
            }
            catch (Exception)
            {
            }
        }
    }
    public class clientInfo
    {
        public int id;
        public string name;
        public string email;
        public string phone;
        public string address;
    }
}
