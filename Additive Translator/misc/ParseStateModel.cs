namespace Additive_Translator.misc
{
    public class ParseStateModel
    {
        public InputModel InputModel { get; set; }

        public ParsingStateEnum State;

        public string InputFile { get; set; }

        public string Id { get; set; }

        public string FileName { get; set; }
    }
}
