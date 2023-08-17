#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

#define INITIAL_ATTRIBUTE_COUNT 100  // Start with a smaller initial allocation
#define ATTRIBUTE_INCREMENT 100     // Increment size when more space is needed

typedef struct {
    char key[100];
    char value[100];
} Attribute;

int reallocate_attributes(Attribute **attributes, int *allocated_size, int new_size) {
    Attribute *new_attributes = realloc(*attributes, new_size * sizeof(Attribute));
    if (!new_attributes) {
        // Handle reallocation failure, for example by breaking out of the loop
        free(*attributes);
        *allocated_size = 0;
        return 0;
    }
    *attributes = new_attributes;
    *allocated_size = new_size;
    return 1;
}

Attribute* extract_attributes(const char *content, int *count) {
    int allocated_size = INITIAL_ATTRIBUTE_COUNT;
    Attribute *attributes = malloc(allocated_size * sizeof(Attribute));

    if (!attributes) {
        *count = 0;
        return NULL;
    }

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

            if (!value_end) break; // Malformed attribute

            int key_length = key_end - key_start + 1;
            int value_length = value_end - value_start;

            if (key_length >= (int) sizeof(attributes[index].key)) {
                key_length = sizeof(attributes[index].key) - 1;
            }
            if (value_length >= (int) sizeof(attributes[index].value)) {
                value_length = sizeof(attributes[index].value) - 1;
            }

            strncpy(attributes[index].key, key_start, key_length);
            attributes[index].key[key_length] = '\0';
            strncpy(attributes[index].value, value_start, value_length);
            attributes[index].value[value_length] = '\0';

            index++;
            if (index == allocated_size) {
                if (!reallocate_attributes(&attributes, &allocated_size, allocated_size + ATTRIBUTE_INCREMENT)) {
                    break;  // Exit the loop if reallocation failed
                }
            }
            attr_pos = value_end + 1;
        }
    }

    *count = index;
    return attributes;
}

Attribute* extract_attributes_from_file(const char *filepath, int *count) {
    FILE *file = fopen(filepath, "rb");
    if (!file) {
        printf("Failed to open file: %s\n", filepath);
        *count = 0;
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    char *content = malloc(file_size + 1);
    if (!content) {
        fclose(file);
        *count = 0;
        return NULL;
    }

    size_t bytes_read = fread(content, 1, file_size, file);
    if (bytes_read < file_size) {
        printf("Failed to read the entire file: %s\n", filepath);
        free(content);
        *count = 0;
        return NULL;
    }

    content[bytes_read] = '\0';  // Use bytes_read to null-terminate
    fclose(file);

    Attribute *attributes = extract_attributes(content, count);
    free(content);
    if (!attributes) {
        printf("No attributes extracted from: %s\n", filepath);
    }
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

            // If count is 0, free the attributes immediately
            if (count == 0) {
                free(attributes);
                attributes = NULL;
            }

            // Skip this file if attribute extraction failed
            if (!attributes) {
                continue;
            }

            Attribute *temp = realloc(all_attributes, (all_attributes_size + count) * sizeof(Attribute));
            if (!temp) {
                printf("Failed to allocate memory for attributes. Skipping file: %s\n", filepath);
                free(attributes);  // ensure the attributes from the current file are freed
                continue;
            }
            all_attributes = temp;

            // Ensure we aren't copying beyond allocated space.
            if (count > 0) {
                memcpy(all_attributes + all_attributes_size, attributes, count * sizeof(Attribute));
                all_attributes_size += count;
            }

            free(attributes);
        }
    }

    closedir(dir);
    *total_count = all_attributes_size;
    return all_attributes;
}