#include <v8.h>

#include <iostream>

%%{
    machine parseInt;
    write data;
}%%


v8::Handle<v8::Value>
parseInt(v8::Arguments const & args) {
    if (args.Length() != 1 || ! args[0]->IsString()) {
        return ThrowException( v8::Exception::Error( v8::String::New(
                        "must be called with one argument (string)")));
    }
    v8::String::Utf8Value str(args[0]->ToString());
    // add one because we want the trailing zero byte
    char *p = *str , *pe = *str + str.length() + 1; 
    int cs;
    int32_t val = 0;
    bool neg = false;

    %%{
        action see_neg {
            neg = true;
        }

        action add_digit { 
            val = val * 10 + (fc - '0');
        }

        main := 
            ( '-'@see_neg | '+' )? ( digit @add_digit )+ 
            '\0';

        # Initialize and execute.
        write init;
        write exec;
    }%%

    if ( neg ) {
        val = -1 * val;
    }

    if ( cs < parseInt_first_final ) {
        std::cerr << "cs:" << cs << " ff:" << parseInt_first_final << std::endl;
        return ThrowException( v8::Exception::Error( v8::String::New(
                        "failed to parse integer")));
    }

    return v8::Number::New(val);
};

extern "C"
void
init(v8::Handle<v8::Object> target) {
    target->Set(
            v8::String::NewSymbol("parseInt"),
            v8::FunctionTemplate::New(parseInt)->GetFunction());
}

