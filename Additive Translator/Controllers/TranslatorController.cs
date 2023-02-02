using System.IO;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using Additive_Translator.Data.Interfaces;
using Additive_Translator.Data.Models;
using Additive_Translator.misc;
using Additive_Translator.Service;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json.Linq;

namespace Additive_Translator.Controllers
{
    [ApiController]
    [Route("api/")]
    public class TranslatorController:ControllerBase
    {
        public readonly FilesHistory _history;
        private readonly FileServise _filseService;

        public TranslatorController(/*IParserFactory parserFactory*/ FilesHistory filesHistory, FileServise filseService )
        {
            _history = filesHistory;
            _filseService = filseService;
            //ParserFactory = parserFactory;
        }


        // private IParserFactory ParserFactory { get; }

        [HttpPost("LoadFile")]
        public async Task<IActionResult> LoadFile(string id, string fName)
        {
            var req = Request.BodyReader;
            var response = await req.ReadAsync();
            var str = Encoding.UTF8.GetString(response.Buffer);
            var localPath = fName.Substring(fName.LastIndexOf('\\') + 1); ;
            _history.History.Add(
                new ParseStateModel() 
                { 
                    Id = (id),
                    FileName = localPath,
                    InputFile = str,
                });
            return Ok();
        }

        [HttpPost("Parse")]
        public async Task<IActionResult> Parce(string id)
        {
            var a = _history.History.Where(c => c.Id.ToString() == id).FirstOrDefault();
            var req = Request.BodyReader;
            var response = await req.ReadAsync();
            var str = Encoding.UTF8.GetString(response.Buffer);
            InputModel? parseModel =
                JsonSerializer.Deserialize<InputModel>(str);
            a.InputModel = parseModel;
            return null;
        }

    }
}