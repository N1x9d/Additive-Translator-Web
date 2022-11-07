using Additive_Translator.Data.Models;

namespace Additive_Translator.Data.Interfaces
{
    public interface ITranslator
    {
        public ParceReqestModel InputData { get; set; }
        public void Process();
    }
}