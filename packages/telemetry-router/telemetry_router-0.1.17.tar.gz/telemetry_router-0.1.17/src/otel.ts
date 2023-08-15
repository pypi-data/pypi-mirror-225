import {
    ConsoleSpanExporter,
    SimpleSpanProcessor
} from "@opentelemetry/sdk-trace-base";
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { WebTracerProvider } from "@opentelemetry/sdk-trace-web";
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions'

export const registerTracerProvider = () => {
    const provider = new WebTracerProvider({
        resource: new Resource({
            [SemanticResourceAttributes.SERVICE_NAME]: "educational-technology-collective"
        }), // set service name
    });

    provider.addSpanProcessor(new SimpleSpanProcessor(new ConsoleSpanExporter())); // print span to console
    provider.addSpanProcessor(new SimpleSpanProcessor(new OTLPTraceExporter({}))); // send to collector (default port 4318)

    provider.register(); // Register this TracerProvider for use with the OpenTelemetry API
}

