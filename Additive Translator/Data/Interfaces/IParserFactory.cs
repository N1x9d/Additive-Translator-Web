using Additive_Translator.Data.Models;

namespace Additive_Translator.Data.Interfaces
{
    public interface IParserFactory
    {
        public void Parce(ParceReqestModel inputParceReqestModel);
    }
}