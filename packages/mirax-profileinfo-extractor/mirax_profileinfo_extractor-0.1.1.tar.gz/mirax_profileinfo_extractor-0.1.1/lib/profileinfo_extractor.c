#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

typedef struct {
    char key[100];
    char value[100];
} Attribute;


Attribute* extract_attributes(const char *content, int *count) {
    char *start = strstr(content, "<data>");
    if (!start) {
        *count = 0;
        return NULL;
    }

    start += strlen("<data>");  // Move the pointer past the <data> tag

    char *end = strstr(start, "</data>");
    if (!end) {
        *count = 0;
        return NULL;
    }

    Attribute *attributes = malloc(100 * sizeof(Attribute)); // assuming maximum 100 attributes
    int index = 0;

    char *pos = start;
    while (pos < end) {
        // Find the next attribute
        char *equal = strchr(pos, '=');
        if (!equal || equal > end) break;

        // Extract key and value
        char *key_end = equal - 1;
        while(*key_end == ' ' || *key_end == '\n' || *key_end == '\t') key_end--;  // skip any whitespace

        char *key_start = key_end;
        while(key_start > pos && *key_start != ' ' && *key_start != '\n' && *key_start != '\t') key_start--;

        // If key_start points to a whitespace character, move to the next character for the start of the key
        if (*key_start == ' ' || *key_start == '\n' || *key_start == '\t') key_start++;

        char *value_start = equal + 2; // skip '=' and the starting quote
        char *value_end = strchr(value_start, '"');

        int key_length = key_end - key_start + 1;
        int value_length = value_end - value_start;

        strncpy(attributes[index].key, key_start, key_length);
        attributes[index].key[key_length] = '\0';
        strncpy(attributes[index].value, value_start, value_length);
        attributes[index].value[value_length] = '\0';

        index++;

        pos = value_end + 1;
    }

    *count = index;
    return attributes;
}

Attribute* extract_attributes_from_file(const char *filepath, int *count) {
    FILE *file = fopen(filepath, "rb");
    if (!file) {
        *count = 0;
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    char *content = malloc(file_size + 1);
    fread(content, file_size, 1, file);
    content[file_size] = '\0';
    fclose(file);

    Attribute *attributes = extract_attributes(content, count);
    free(content);
    return attributes;
}

Attribute* extract_attributes_from_directory(const char *directory, int *total_count) {
    DIR *dir = opendir(directory);
    if (!dir) {
        *total_count = 0;
        return NULL;
    }

    Attribute *all_attributes = NULL;
    int all_attributes_size = 0;
    struct dirent *entry;

    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) {  // If it's a regular file
            char filepath[1024];
            snprintf(filepath, sizeof(filepath), "%s/%s", directory, entry->d_name);

            int count;
            Attribute *attributes = extract_attributes_from_file(filepath, &count);

            all_attributes = realloc(all_attributes, (all_attributes_size + count) * sizeof(Attribute));
            memcpy(all_attributes + all_attributes_size, attributes, count * sizeof(Attribute));
            all_attributes_size += count;

            free(attributes);
        }
    }

    closedir(dir);
    *total_count = all_attributes_size;
    return all_attributes;
}
