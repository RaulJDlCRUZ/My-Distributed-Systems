module URFS {  // Unified Remote File System

  struct FileInfo {
    string name;
    string hash;
  };

  exception FileNameInUseError {};
  exception FileNotFoundError {};
  exception FileAlreadyExistsError {
    string hash;
  };

  sequence<FileInfo> FileList;

  interface Uploader {
    void send(string data);
    FileInfo save()
      throws FileAlreadyExistsError;
    void destroy();
  };

  interface Downloader {
    string recv(int size);
    void destroy();
  };

  interface FileManager {
    Uploader* createUploader(string filename);
    Downloader* createDownloader(string hash)
      throws FileNotFoundError;
    void removeFile(string hash)
      throws FileNotFoundError;
  };

  interface Frontend {
    FileList getFileList();
    Uploader* uploadFile(string filename)
      throws FileNameInUseError;
    Downloader* downloadFile(string hash)
      throws FileNotFoundError;
    FileInfo getFileInfo(string hash)
      throws FileNotFoundError;
    void removeFile(string hash)
      throws FileNotFoundError;

    void replyNewFrontend(Frontend* oldFrontend);
  };

  interface FrontendUpdates {
    void newFrontend(Frontend* newFrontend);
  };

  struct FileData {
    FileInfo fileInfo;
    FileManager* fileManager;
  };

  interface FileUpdates {
    void new(FileData file);
    void removed(FileData file);
  };

};
