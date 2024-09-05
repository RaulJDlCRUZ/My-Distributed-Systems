module Example {
  interface Printer {
    void write(string message);
    void destroy();
  };

  interface PrinterFactory {
    Printer* create(string name);
  };
};
