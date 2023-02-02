namespace Additive_Translator.Service
{
    public class FileServise
    {
        public async Task<string> WriteInputFileAsync(string input, string fName, string id)
        {
            if (!Directory.Exists("Uploads"))
            {
                Directory.CreateDirectory("Uploads");
            }
           
            var sp = Directory.GetCurrentDirectory();
            var savePath = Path.Combine("Uploads", id, fn);
            await using var stream = File.Create(savePath);
            using (var sw = new StreamWriter(savePath))
            {
                sw.Write(input);
            }
            return savePath;
        }
    }
}
