#include <stdio.h>
#include <gtk/gtk.h>

/**
 * Save Dialogue Test Program.
 *
 * Click the Save button and a GtkFileChooserDialog is shown.
 *
 * When the save is activated, the location a file would be saved to
 * is printed to stdout.
 */

/**
 * Based on http://developer.gnome.org/gtk3/3.0/gtk-getting-started.html
 * hello world example.
 */

static void save(GtkWidget *widget, gpointer data);
static gboolean on_delete_event(GtkWidget *widget, GdkEvent *event, gpointer data);
static void save_to_file(char* filename);

int main(int argc, char **argv) {
    GtkWidget *window;
    GtkWidget *button;

    gtk_init(&argc, &argv);

    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), "Save Example");

    //g_signal_connect(window, "delete-event", G_CALLBACK(on_delete_event), NULL);
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);

    gtk_container_set_border_width(GTK_CONTAINER (window), 10);

    button = gtk_button_new_with_label("Save");

    g_signal_connect(button, "clicked", G_CALLBACK(save), window);
    //g_signal_connect_swapped(button, "clicked", G_CALLBACK(gtk_widget_destroy), window);

    gtk_container_add(GTK_CONTAINER(window), button);

    gtk_widget_show(button);

    gtk_widget_show(window);

    gtk_main();
    return 0;
}

static void save(GtkWidget *widget, gpointer data) {
    GtkWidget *dialog;

    dialog = gtk_file_chooser_dialog_new(
        "Save File",
        GTK_WINDOW(data),
        GTK_FILE_CHOOSER_ACTION_SAVE,
        GTK_STOCK_CANCEL, GTK_RESPONSE_CANCEL,
        GTK_STOCK_SAVE, GTK_RESPONSE_ACCEPT,
        NULL
    );

    gtk_file_chooser_set_do_overwrite_confirmation(GTK_FILE_CHOOSER(dialog), TRUE);

    gtk_file_chooser_set_current_name(GTK_FILE_CHOOSER(dialog), "Untitled");

    if (gtk_dialog_run(GTK_DIALOG(dialog)) == GTK_RESPONSE_ACCEPT) {
        char *filename;
        filename = gtk_file_chooser_get_filename(GTK_FILE_CHOOSER(dialog));
        save_to_file(filename);
        g_free(filename);
    }
    gtk_widget_destroy(dialog);
}

static void save_to_file(char* filename) {
    printf("Would save '%s'\n", filename);
}

static gboolean on_delete_event(GtkWidget *widget, GdkEvent *event, gpointer data) {
  /* If you return FALSE in the "delete_event" signal handler,
   * GTK will emit the "destroy" signal. Returning TRUE means
   * you don't want the window to be destroyed.
   *
   * This is useful for popping up 'are you sure you want to quit?'
   * type dialogs.
   */
    g_print("delete event occurred\n");

    return TRUE;
}
