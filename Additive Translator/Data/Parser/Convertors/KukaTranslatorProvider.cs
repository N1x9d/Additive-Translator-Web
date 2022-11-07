using Additive_Translator.Data.Interfaces;
using Additive_Translator.Data.Models;

namespace Additive_Translator.Data.Parser.Convertors
{
    public class KukaTranslatorProvider : ITranslator
    {
        private KukaDTO kukaDTO;
        public ParceReqestModel InputData { get; set; }

        public KukaTranslatorProvider(ParceReqestModel inputParceReqestModel)
        {
            kukaDTO = new KukaDTO(inputParceReqestModel);
            InputData = inputParceReqestModel;
        }

        public void Process()
        {
            throw new NotImplementedException();
        }

        internal class KukaDTO
        {
            public KukaDTO(ParceReqestModel inputParceReqestModel)
            {
                UF = inputParceReqestModel.Uf;
                UT = inputParceReqestModel.Ut;
                Input = inputParceReqestModel.InputFilePath;
                Output = inputParceReqestModel.OutputFile; 
                MaxPoints = 500;
            }

            public uint UF { get; set; }
            public uint UT { get; set; }
            public string Input { get; set; }
            public string Output { get; set; }

            public uint MaxPoints { get; set; }
        }
    }
}
