using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.IO;
using System.Xml;
using System.Net;
using Microsoft.Office.Interop.Excel;

namespace SSID
{
    class Program
    {
        static void Main(string[] args)
        {
            Microsoft.Office.Interop.Excel.Application excel = new Microsoft.Office.Interop.Excel.Application();
            if (excel == null)
            {
                Console.WriteLine("Excel bulunamadı. \n");
                goto son;
            }
            
            Console.WriteLine("[{0}] İşlem Başladı.", DateTime.Now);

            string path = Directory.GetCurrentDirectory();
            string hedef = path + "\\SSID";
            Directory.CreateDirectory(hedef);

            Process islem = new System.Diagnostics.Process();
            islem.StartInfo.FileName = "cmd.exe";
            islem.StartInfo.Verb = "runas";
            islem.StartInfo.Arguments = "/c netsh wlan export profile folder=" + hedef + " key=clear";
            islem.Start();
            islem.WaitForExit();

            SortedList SSID = new SortedList();
            string key;
            bool has;
            string[] files = Directory.GetFiles(hedef);
            foreach (string filename in files)
            {
                key = "";
                has = false;
                XmlReader oXr = XmlReader.Create(@filename);
                while (oXr.Read())
                {
                    if (oXr.Name == "name") has = true;
                    if (has == true && oXr.HasValue)
                    {
                        key = oXr.Value;
                        SSID[key] = "";
                        has = false;
                        break;
                    }
                }
                while (oXr.Read())
                {
                    if (oXr.Name == "keyMaterial") has = true;
                    if (has == true && oXr.HasValue)
                    {
                        SSID[key] = oXr.Value;
                        break;
                    }
                }
                oXr.Close();
            }

            Directory.Delete(hedef, true);

            Console.WriteLine("[{0}] Tüm bilgiler SSIDFile.xlsx dosyasına kaydediliyor.", DateTime.Now);
            
            Workbook workbook;
            hedef = path + "\\SSIDFile.xlsx";
            if (File.Exists(hedef)) workbook = excel.Workbooks.Open(hedef);
            else
            {
                workbook = excel.Workbooks.Add();
                workbook.SaveAs(hedef);
            }
            Worksheet sheet1 = (Worksheet)workbook.Sheets[1];
            sheet1.Cells[1, 1].Value = "SSID";
            sheet1.Cells[1, 2].Value = "PASSWORD";
            Range area = sheet1.get_Range("A1", "B1");
            area.Font.Bold = true;
            int row = 1;
            while (sheet1.Cells[++row, 1].Value != null);
            foreach (string id in SSID.Keys)
            {                
                sheet1.Cells[row, 1].Value = id;
                sheet1.Cells[row, 2].Value = SSID[id];
                row++;
            }
            sheet1.Columns.HorizontalAlignment = 3; // Center
            sheet1.Columns.AutoFit();
            workbook.Save();
            excel.Quit();

            Console.WriteLine("[{0}] İşlem Tamamlandı. \n", DateTime.Now);

            son :
            Console.WriteLine("Mehmet Selçuk Çalışkan (210541099) \n");
            Console.Write("Enter tuşuna basarak uygulamayı sonlandırabilirsiniz.");
            Console.ReadLine();
        }
    }
}