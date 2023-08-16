#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

typedef struct {
    char key[100];
    char value[100];
} Attribute;

Attribute* extract_attributes(const char *content, int *count) {
    Attribute *attributes = malloc(500 * sizeof(Attribute)); // assuming maximum 500 attributes
    int index = 0;
    const char *pos = content;

    while (pos && *pos) {
        char *start = strchr(pos, '<'); // Find the start of any tag

        if (!start) break;  // No more tags found

        char *end = strchr(start, '>'); // Find the end of this tag

        if (!end) break;  // Malformed XML

        char *self_closing = strstr(start, "/>"); // Check if it's a self-closing tag
        if (self_closing && self_closing < end) {
            end = self_closing;
        }

        pos = end + 1;

        char *attr_pos = start + 1;
        while (attr_pos < end) {
            char *equal = strchr(attr_pos, '=');
            if (!equal || equal > end) break;

            char *key_end = equal - 1;
            while(*key_end == ' ' || *key_end == '\n' || *key_end == '\t') key_end--;

            char *key_start = key_end;
            while(key_start > attr_pos && *key_start != ' ' && *key_start != '\n' && *key_start != '\t') key_start--;

            if (*key_start == ' ' || *key_start == '\n' || *key_start == '\t') key_start++;

            char *value_start = equal + 2;
            char *value_end = strchr(value_start, '"');

            int key_length = key_end - key_start + 1;
            int value_length = value_end - value_start;

            strncpy(attributes[index].key, key_start, key_length);
            attributes[index].key[key_length] = '\0';
            strncpy(attributes[index].value, value_start, value_length);
            attributes[index].value[value_length] = '\0';

            index++;
            attr_pos = value_end + 1;
        }
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
    // Free all_attributes in the caller (Python code)
    return all_attributes;
}
