module Example {
  interface Intermediary {
    void send(string message, string destinationProxy);
  };

  interface Printer {
    void write(string message);
  };
};